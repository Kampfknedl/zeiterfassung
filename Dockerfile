FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV ANDROID_SDK_ROOT=/opt/android-sdk
ENV ANDROID_NDK_ROOT=/opt/android-ndk
ENV GRADLE_USER_HOME=/root/.gradle

# System dependencies - optimized for faster builds
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.10 python3.10-dev python3.10-distutils python3-pip \
    openjdk-17-jdk \
    git zip unzip wget curl \
    build-essential cmake autoconf automake libtool pkg-config \
    libssl-dev libffi-dev libsqlite3-dev \
    zlib1g-dev libbz2-dev libreadline-dev \
    ccache \
    && rm -rf /var/lib/apt/lists/*

# Python toolchain - with cache optimization
RUN python3.10 -m pip install --upgrade pip setuptools wheel
RUN python3.10 -m pip install --no-cache-dir "cython<3" "buildozer>=1.5.0"

# Android command line tools
RUN mkdir -p /opt/android-sdk/cmdline-tools && \
    wget -q https://dl.google.com/android/repository/commandlinetools-linux-11076708_latest.zip -O /tmp/tools.zip && \
    unzip /tmp/tools.zip -d /opt/android-sdk/cmdline-tools && \
    mv /opt/android-sdk/cmdline-tools/cmdline-tools /opt/android-sdk/cmdline-tools/latest && \
    rm /tmp/tools.zip && \
    mkdir -p /opt/android-sdk/tools/bin && \
    ln -s /opt/android-sdk/cmdline-tools/latest/bin/sdkmanager /opt/android-sdk/tools/bin/sdkmanager

# Android NDK r25b (stable for p4a/buildozer)
RUN wget -q https://dl.google.com/android/repository/android-ndk-r25b-linux.zip -O /tmp/ndk.zip && \
    unzip /tmp/ndk.zip -d /opt && \
    mv /opt/android-ndk-r25b /opt/android-ndk && \
    rm /tmp/ndk.zip

# Add SDK tools to PATH
ENV PATH="$ANDROID_SDK_ROOT/cmdline-tools/latest/bin:$ANDROID_SDK_ROOT/platform-tools:$PATH"

# Accept licenses and install platforms/build-tools
RUN yes | sdkmanager --licenses 2>&1 | grep -v "Warning:" || true
RUN sdkmanager "platform-tools" "platforms;android-21" "platforms;android-34" "build-tools;34.0.0" 2>&1 | grep -v "Warning:" || true

# Gradle optimization
RUN mkdir -p /root/.gradle && \
    echo "org.gradle.jvmargs=-Xmx2048m" > /root/.gradle/gradle.properties && \
    echo "org.gradle.parallel=true" >> /root/.gradle/gradle.properties && \
    echo "org.gradle.workers.max=4" >> /root/.gradle/gradle.properties

WORKDIR /app
CMD ["bash"]
