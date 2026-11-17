import os

def f(path, lines):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as file:
        file.write("\n".join(lines) + "\n")

f("build.gradle", [
    "buildscript {",
    "    repositories { google(); mavenCentral() }",
    "    dependencies {",
    "        classpath 'com.android.tools.build:gradle:8.2.0'",
    "        classpath 'org.jetbrains.kotlin:kotlin-gradle-plugin:1.9.20'",
    "    }",
    "}",
    "allprojects { repositories { google(); mavenCentral() } }"
])

f("settings.gradle", [
    "pluginManagement { repositories { google(); mavenCentral(); gradlePluginPortal() } }",
    "dependencyResolutionManagement {",
    "    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)",
    "    repositories { google(); mavenCentral() }",
    "}",
    "rootProject.name = 'KinoClub'",
    "include ':app'"
])

f("app/build.gradle", [
    "plugins {",
    "    id 'com.android.application'",
    "    id 'org.jetbrains.kotlin.android'",
    "}",
    "android {",
    "    namespace 'com.kinoclub.app'",
    "    compileSdk 34",
    "    defaultConfig {",
    "        applicationId 'com.kinoclub.app'",
    "        minSdk 24",
    "        targetSdk 34",
    "        versionCode 1",
    "        versionName '1.0'",
    "    }",
    "    compileOptions {",
    "        sourceCompatibility JavaVersion.VERSION_17",
    "        targetCompatibility JavaVersion.VERSION_17",
    "    }",
    "    kotlinOptions { jvmTarget = '17' }",
    "    buildFeatures { compose true }",
    "    composeOptions { kotlinCompilerExtensionVersion '1.5.4' }",
    "}",
    "dependencies {",
    "    implementation 'androidx.core:core-ktx:1.12.0'",
    "    implementation 'androidx.lifecycle:lifecycle-runtime-ktx:2.7.0'",
    "    implementation 'androidx.activity:activity-compose:1.8.2'",
    "    implementation platform('androidx.compose:compose-bom:2023.10.01')",
    "    implementation 'androidx.compose.ui:ui'",
    "    implementation 'androidx.compose.ui:ui-graphics'",
    "    implementation 'androidx.compose.ui:ui-tooling-preview'",
    "    implementation 'androidx.compose.material3:material3'",
    "    implementation 'androidx.media3:media3-exoplayer:1.2.0'",
    "    implementation 'androidx.media3:media3-exoplayer-hls:1.2.0'",
    "    implementation 'androidx.media3:media3-ui:1.2.0'",
    "    implementation 'io.coil-kt:coil-compose:2.5.0'",
    "}"
])

f("app/src/main/AndroidManifest.xml", [
    "<manifest xmlns:android='http://schemas.android.com/apk/res/android'>",
    "    <uses-permission android:name='android.permission.INTERNET' />",
    "    <application android:allowBackup='true' android:icon='@mipmap/ic_launcher' android:label='KINO-CLUB' android:theme='@style/Theme.KinoClub'>",
    "        <activity android:name='.MainActivity' android:exported='true' android:configChanges='orientation|screenSize'>",
    "            <intent-filter>",
    "                <action android:name='android.intent.action.MAIN' />",
    "                <category android:name='android.intent.category.LAUNCHER' />",
    "            </intent-filter>",
    "        </activity>",
    "    </application>",
    "</manifest>"
])

f("app/src/main/res/values/themes.xml", [
    "<resources>",
    "    <style name='Theme.KinoClub' parent='Theme.Material3.Dark.NoActionBar' />",
    "</resources>"
])

f("app/src/main/java/com/kinoclub/app/MainActivity.kt", [
    "package com.kinoclub.app",
    "import android.os.Bundle",
    "import androidx.activity.ComponentActivity",
    "import androidx.activity.compose.setContent",
    "import androidx.compose.material3.Surface",
    "import androidx.compose.material3.Text",
    "import androidx.compose.ui.graphics.Color",
    "class MainActivity : ComponentActivity() {",
    "    override fun onCreate(savedInstanceState: Bundle?) {",
    "        super.onCreate(savedInstanceState)",
    "        setContent { Surface(color = Color.Black) { Text('KINO-CLUB Ready', color = Color.White) } }",
    "    ",
    "}",
    "}"
])

print("OK")
