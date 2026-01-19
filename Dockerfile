FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV ANDROID_SDK_ROOT=/opt/android-sdk
ENV ANDROID_NDK_ROOT=/opt/android-ndk

# System dependencies
RUN apt-get update && apt-get install -y \
    python3.10 python3.10-dev python3.10-distutils python3-pip \
    openjdk-17-jdk \
    git zip unzip wget curl \
    build-essential cmake autoconf automake libtool pkg-config \
    libssl-dev libffi-dev libsqlite3-dev \
    zlib1g-dev libbz2-dev libreadline-dev \
    && rm -rf /var/lib/apt/lists/*

# Python toolchain
RUN python3.10 -m pip install --upgrade pip
RUN python3.10 -m pip install --no-cache-dir "cython<3" buildozer

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
RUN yes | sdkmanager --licenses
RUN sdkmanager "platform-tools" "platforms;android-34" "build-tools;34.0.0"

WORKDIR /app
CMD ["bash"]
