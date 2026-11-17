name: Build KINO-CLUB APK

on:
  push:
    branches: [ "main", "master" ]
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout
      uses: actions/checkout@v4

    - name: Setup Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.11'

    - name: Run Builder
      run: python setup_and_build.py

    - name: Setup JDK 17
      uses: actions/setup-java@v4
      with:
        distribution: 'temurin'
        java-version: '17'

    - name: Setup Gradle
      uses: gradle/actions/setup-gradle@v4
      with:
        gradle-version: '8.7'

    - name: Build APK
      run: gradle assembleDebug

    - name: Upload Artifact
      uses: actions/upload-artifact@v4
      with:
        name: KINO-CLUB-app
        path: app/build/outputs/apk/debug/app-debug.apk
            
