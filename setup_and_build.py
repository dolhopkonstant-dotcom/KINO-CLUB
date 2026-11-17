import os

files = {
    "settings.gradle.kts": """pluginManagement {
    repositories {
        google()
        mavenCentral()
        gradlePluginPortal()
    }
}
dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {
        google()
        mavenCentral()
    }
}

rootProject.name = "KinoClub"
include(":app")
""",
    "build.gradle.kts": """plugins {
    id("com.android.application") version "8.5.2" apply false
    id("org.jetbrains.kotlin.android") version "1.9.24" apply false
}
""",
    "gradle.properties": """org.gradle.jvmargs=-Xmx2048m -Dfile.encoding=UTF-8
android.useAndroidX=true
kotlin.code.style=official
android.nonTransitiveRClass=true
""",
    "app/proguard-rules.pro": "# ProGuard rules\n",
    "app/build.gradle.kts": """plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
}

android {
    namespace = "com.kostya.kinoclub"
    compileSdk = 34

    defaultConfig {
        applicationId = "com.kostya.kinoclub"
        minSdk = 24
        targetSdk = 34
        versionCode = 1
        versionName = "1.0"
    }

    buildTypes {
        release {
            isMinifyEnabled = false
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
        }
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
    kotlinOptions {
        jvmTarget = "17"
    }
    buildFeatures {
        compose = true
    }
    composeOptions {
        kotlinCompilerExtensionVersion = "1.5.14"
    }
}

dependencies {
    implementation("androidx.core:core-ktx:1.13.1")
    implementation("androidx.lifecycle:lifecycle-runtime-ktx:2.8.4")
    implementation("androidx.activity:activity-compose:1.9.1")
    implementation(platform("androidx.compose:compose-bom:2024.06.00"))
    implementation("androidx.compose.ui:ui")
    implementation("androidx.compose.ui:ui-graphics")
    implementation("androidx.compose.ui:ui-tooling-preview")
    implementation("androidx.compose.material3:material3")
    implementation("androidx.compose.material:material-icons-extended")

    val media3Version = "1.4.1"
    implementation("androidx.media3:media3-exoplayer:$media3Version")
    implementation("androidx.media3:media3-exoplayer-hls:$media3Version")
    implementation("androidx.media3:media3-ui:$media3Version")

    implementation("io.coil-kt:coil-compose:2.6.0")
}
""",
    "app/src/main/AndroidManifest.xml": """<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android">

    <uses-permission android:name="android.permission.INTERNET" />

    <application
        android:allowBackup="true"
        android:label="KINO-CLUB"
        android:supportsRtl="true"
        android:theme="@android:style/Theme.Material.NoActionBar">
        <activity
            android:name=".MainActivity"
            android:exported="true"
            android:configChanges="orientation|screenSize|screenLayout|keyboardHidden">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>

</manifest>
""",
    "app/src/main/java/com/kostya/kinoclub/Models.kt": """package com.kostya.kinoclub

data class User(
    val id: String,
    val hasActiveSubscription: Boolean
)

data class MediaContent(
    val id: String,
    val title: String,
    val description: String,
    val authorName: String,
    val isSeries: Boolean,
    val isFreeMovie: Boolean = false,
    val episodes: List<Episode> = emptyList()
)

data class Episode(
    val number: Int,
    val title: String,
    val videoStreamUrl: String
)

fun canWatchContent(user: User, content: MediaContent, episodeNumber: Int = 1): Boolean {
    if (user.hasActiveSubscription) return true
    if (!content.isSeries && content.isFreeMovie) return true
    if (content.isSeries && episodeNumber == 1) return true
    return false
}

val sampleCatalog = listOf(
    MediaContent(
        id = "movie_1",
        title = "Ночной дрифт (Бесплатный фильм)",
        description = "Авторский фильм о ночных заездах. Доступен бесплатно для ознакомления.",
        authorName = "Автор: StudioDrift",
        isSeries = false,
        isFreeMovie = true,
        episodes = listOf(
            Episode(1, "Полный фильм", "https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8")
        )
    ),
    MediaContent(
        id = "series_1",
        title = "Тайны Сибири (Сериал)",
        description = "Независимый детективный сериал. 1-я серия бесплатно, продолжение — по подписке 150 ₽/мес.",
        authorName = "Автор: SiberiaFilm",
        isSeries = true,
        isFreeMovie = false,
        episodes = listOf(
            Episode(1, "Серия 1: Начало (Бесплатно)", "https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8"),
            Episode(2, "Серия 2: След в тайге", "https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8"),
            Episode(3, "Серия 3: Развязка", "https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8")
        )
    ),
    MediaContent(
        id = "movie_2",
        title = "Гараж мечты (По подписке)",
        description = "Полнометражный авторский проект о восстановлении редких авто.",
        authorName = "Автор: AutoMasters",
        isSeries = false,
        isFreeMovie = false,
        episodes = listOf(
            Episode(1, "Полный фильм", "https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8")
        )
    )
)
""",
    "app/src/main/java/com/kostya/kinoclub/VideoPlayerScreen.kt": """package com.kostya.kinoclub

import android.net.Uri
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.Flag
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.unit.dp
import androidx.compose.ui.viewinterop.AndroidView
import androidx.media3.common.MediaItem
import androidx.media3.exoplayer.ExoPlayer
import androidx.media3.ui.PlayerView

@Composable
fun VideoPlayerScreen(
    title: String,
    videoUrl: String,
    onBack: () -> Unit,
    onReport: () -> Unit
) {
    val context = LocalContext.current

    val exoPlayer = remember(videoUrl) {
        ExoPlayer.Builder(context).build().apply {
            val mediaItem = MediaItem.fromUri(Uri.parse(videoUrl))
            setMediaItem(mediaItem)
            prepare()
            playWhenReady = true
        }
    }

    DisposableEffect(Unit) {
        onDispose {
            exoPlayer.release()
        }
    }

    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(Color.Black)
    ) {
        AndroidView(
            factory = { ctx ->
                PlayerView(ctx).apply {
                    player = exoPlayer
                    useController = true
                }
            },
            modifier = Modifier.fillMaxSize()
        )

        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp)
                .align(Alignment.TopCenter),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {
            IconButton(onClick = onBack) {
                Icon(
                    imageVector = Icons.AutoMirrored.Filled.ArrowBack,
                    contentDescription = "Назад",
                    tint = Color.White
                )
            }
            Text(text = title, color = Color.White, style = MaterialTheme.typography.titleMedium)
            IconButton(onClick = onReport) {
                Icon(
                    imageVector = Icons.Default.Flag,
                    contentDescription = "Пожаловаться",
                    tint = Color.Red
                )
            }
        }
    }
}
""",
    "app/src/main/java/com/kostya/kinoclub/MainActivity.kt": """package com.kostya.kinoclub

import android.os.Bundle
import android.widget.Toast
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Lock
import androidx.compose.material.icons.filled.PlayArrow
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            MaterialTheme(colorScheme = darkColorScheme()) {
                CinemaAppMain()
            }
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun CinemaAppMain() {
    val context = LocalContext.current
    var user by remember { mutableStateOf(User(id = "user_1", hasActiveSubscription = false)) }
    var selectedContent by remember { mutableStateOf<MediaContent?>(null) }
    var playingEpisode by remember { mutableStateOf<Pair<String, String>?>(null) }
    var showPaywall by remember { mutableStateOf(false) }

    if (playingEpisode != null) {
        VideoPlayerScreen(
            title = playingEpisode!!.first,
            videoUrl = playingEpisode!!.second,
            onBack = { playingEpisode = null },
            onReport = {
                Toast.makeText(context, "Жалоба отправлена модератору", Toast.LENGTH_SHORT).show()
            }
        )
        return
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("KINO-CLUB") },
                actions = {
                    if (user.hasActiveSubscription) {
                        Text(
                            text = "Подписка активна",
                            color = Color(0xFF4CAF50),
                            modifier = Modifier.padding(end = 16.dp),
                            fontWeight = FontWeight.Bold
                        )
                    } else {
                        Button(
                            onClick = { showPaywall = true },
                            modifier = Modifier.padding(end = 8.dp)
                        ) {
                            Text("150 ₽/мес")
                        }
                    }
                }
            )
        }
    ) { padding ->
        if (selectedContent == null) {
            LazyColumn(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(padding)
                    .padding(16.dp),
                verticalArrangement = Arrangement.spacedBy(12.dp)
            ) {
                items(sampleCatalog) { item ->
                    Card(
                        modifier = Modifier
                            .fillMaxWidth()
                            .clickable { selectedContent = item },
                        shape = RoundedCornerShape(12.dp)
                    ) {
                        Column(modifier = Modifier.padding(16.dp)) {
                            Text(item.title, style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold)
                            Spacer(modifier = Modifier.height(4.dp))
                            Text(item.authorName, style = MaterialTheme.typography.labelMedium, color = Color.Gray)
                            Spacer(modifier = Modifier.height(8.dp))
                            Text(item.description, style = MaterialTheme.typography.bodyMedium)
                        }
                    }
                }
            }
        } else {
            val content = selectedContent!!
            Column(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(padding)
                    .padding(16.dp)
            ) {
                TextButton(onClick = { selectedContent = null }) {
                    Text("← Назад в каталог")
                }
                Text(content.title, style = MaterialTheme.typography.headlineSmall, fontWeight = FontWeight.Bold)
                Text(content.authorName, color = Color.Gray)
                Spacer(modifier = Modifier.height(8.dp))
                Text(content.description)
                Spacer(modifier = Modifier.height(16.dp))
                Text("Доступные видео:", style = MaterialTheme.typography.titleMedium)
                Spacer(modifier = Modifier.height(8.dp))

                content.episodes.forEach { ep ->
                    val allowed = canWatchContent(user, content, ep.number)
                    Card(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(vertical = 4.dp)
                            .clickable {
                                if (allowed) {
                                    playingEpisode = Pair("${content.title} - ${ep.title}", ep.videoStreamUrl)
                                } else {
                                    showPaywall = true
                                }
                            }
                    ) {
                        Row(
                            modifier = Modifier
                                .fillMaxWidth()
                                .padding(16.dp),
                            horizontalArrangement = Arrangement.SpaceBetween,
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Text(ep.title, fontWeight = FontWeight.Medium)
                            Icon(
                                imageVector = if (allowed) Icons.Default.PlayArrow else Icons.Default.Lock,
                                contentDescription = null,
                                tint = if (allowed) Color(0xFF4CAF50) else Color(0xFFFF9800)
                            )
                        }
                    }
                }
            }
        }
    }

    if (showPaywall) {
        AlertDialog(
            onDismissRequest = { showPaywall = false },
            title = { Text("Подписка KINO-CLUB") },
            text = {
                Text("Полный доступ ко всем авторским фильмам и сериалам всего за 150 ₽ в месяц. Бесплатно доступны 1 ознакомительный фильм и 1-я серия любого сериала.")
            },
            confirmButton = {
                Button(onClick = {
                    user = user.copy(hasActiveSubscription = true)
                    showPaywall = false
                    Toast.makeText(context, "Подписка на 30 дней активирована!", Toast.LENGTH_LONG).show()
                }) {
                    Text("Оплатить 150 ₽")
                }
            },
            dismissButton = {
                TextButton(onClick = { showPaywall = false }) {
                    Text("Отмена")
                }
            }
        )
    }
}
"""
}

for path, content in files.items():
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

print("All Android project files generated successfully!")
