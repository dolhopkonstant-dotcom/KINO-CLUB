import os

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

print("Starting project generation...")

# 1. Gradle configs
write_file("build.gradle", """buildscript {
    repositories { google(); mavenCentral() }
    dependencies {
        classpath 'com.android.tools.build:gradle:8.2.0'
        classpath "org.jetbrains.kotlin:kotlin-gradle-plugin:1.9.20"
    }
}
allprojects { repositories { google(); mavenCentral() } }
""")

write_file("settings.gradle", """pluginManagement {
    repositories { google(); mavenCentral(); gradlePluginPortal() }
}
dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories { google(); mavenCentral() }
}
rootProject.name = "KinoClub"
include ':app'
""")

write_file("app/build.gradle", """plugins {
    id 'com.android.application'
    id 'org.jetbrains.kotlin.android'
}
android {
    namespace 'com.kinoclub.app'
    compileSdk 34
    defaultConfig {
        applicationId "com.kinoclub.app"
        minSdk 24
        targetSdk 34
        versionCode 1
        versionName "1.0"
    }
    compileOptions {
        sourceCompatibility JavaVersion.VERSION_17
        targetCompatibility JavaVersion.VERSION_17
    }
    kotlinOptions { jvmTarget = '17' }
    buildFeatures { compose true }
    composeOptions { kotlinCompilerExtensionVersion '1.5.4' }
}
dependencies {
    implementation 'androidx.core:core-ktx:1.12.0'
    implementation 'androidx.lifecycle:lifecycle-runtime-ktx:2.7.0'
    implementation 'androidx.activity:activity-compose:1.8.2'
    implementation platform('androidx.compose:compose-bom:2023.10.01')
    implementation 'androidx.compose.ui:ui'
    implementation 'androidx.compose.ui:ui-graphics'
    implementation 'androidx.compose.ui:ui-tooling-preview'
    implementation 'androidx.compose.material3:material3'
    implementation 'androidx.compose.material:material-icons-extended'
    implementation 'androidx.media3:media3-exoplayer:1.2.0'
    implementation 'androidx.media3:media3-exoplayer-hls:1.2.0'
    implementation 'androidx.media3:media3-ui:1.2.0'
    implementation 'io.coil-kt:coil-compose:2.5.0'
}
""")

write_file("app/src/main/AndroidManifest.xml", """<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android">
    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="KINO-CLUB"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/Theme.KinoClub">
        <activity
            android:name=".MainActivity"
            android:exported="true"
            android:screenOrientation="unspecified"
            android:configChanges="orientation|screenSize|keyboardHidden">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
""")

write_file("app/src/main/res/values/themes.xml", """<resources>
    <style name="Theme.KinoClub" parent="Theme.Material3.Dark.NoActionBar">
        <item name="android:statusBarColor">@android:color/black</item>
        <item name="android:navigationBarColor">@android:color/black</item>
    </style>
</resources>
""")

# 2. Kotlin App Code
write_file("app/src/main/java/com/kinoclub/app/MainActivity.kt", """package com.kinoclub.app

import android.app.Activity
import android.content.pm.ActivityInfo
import android.content.res.Configuration
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.*
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalConfiguration
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.viewinterop.AndroidView
import androidx.media3.common.MediaItem
import androidx.media3.exoplayer.ExoPlayer
import androidx.media3.ui.PlayerView
import coil.compose.AsyncImage

data class Episode(val id: Int, val title: String, val videoUrl: String, val isFree: Boolean)
data class Movie(val id: Int, val title: String, val type: String, val author: String, val description: String, val posterRes: String, val genre: String, val episodes: List<Episode>)

object MockRepository {
    val movies = listOf(
        Movie(1, "Ночной дрифт", "Фильм", "StudioDrift", "Авторский фильм о ночных заездах и тюнинге.", "https://images.unsplash.com/photo-1503376780353-7e6692767b70?w=600", "Экшн", listOf(Episode(1, "Полнометражный фильм", "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4", true))),
        Movie(2, "Тайны Сибири", "Сериал", "SiberiaFilm", "Детективный сериал об экспедиции в тайгу. 1-я серия бесплатно.", "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=600", "Детектив", listOf(
            Episode(1, "Серия 1", "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4", true),
            Episode(2, "Серия 2", "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4", false)
        ))
    )
}

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            Surface(modifier = Modifier.fillMaxSize(), color = Color(0xFF0F0F13)) {
                MainApp()
            }
        }
    }
}

@Composable
fun MainApp() {
    var selectedMovie by remember { mutableStateOf<Movie?>(null) }
    var activeEpisode by remember { mutableStateOf<Episode?>(null) }
    var isSubscribed by remember { mutableStateOf(false) }
    var showPaywall by remember { mutableStateOf(false) }

    if (activeEpisode != null) {
        PlayerScreen(episode = activeEpisode!!) { activeEpisode = null }
    } else if (selectedMovie != null) {
        DetailScreen(movie = selectedMovie!!, isSubscribed = isSubscribed, onBack = { selectedMovie = null }) { ep ->
            if (ep.isFree || isSubscribed) activeEpisode = ep else showPaywall = true
        }
    } else {
        HomeScreen(movies = MockRepository.movies, isSubscribed = isSubscribed, onMovieClick = { selectedMovie = it }) { showPaywall = true }
    }

    if (showPaywall) {
        AlertDialog(
            onDismissRequest = { showPaywall = false },
            containerColor = Color(0xFF1A1A24),
            title = { Text("Подписка KINO-CLUB", color = Color.White) },
            text = { Text("Полный доступ ко всем фильмам и сериалам за 150 ₽/мес.", color = Color.LightGray) },
            confirmButton = {
                Button(onClick = { isSubscribed = true; showPaywall = false }, colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF9333EA))) {
                    Text("Оформить за 150 ₽", color = Color.White)
                }
            },
            dismissButton = { TextButton(onClick = { showPaywall = false }) { Text("Отмена", color = Color.Gray) } }
        )
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun HomeScreen(movies: List<Movie>, isSubscribed: Boolean, onMovieClick: (Movie) -> Unit, onSubscribeClick: () -> Unit) {
    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("KINO-CLUB", color = Color.White, fontWeight = FontWeight.Bold) },
                colors = TopAppBarDefaults.topAppBarColors(containerColor = Color(0xFF16161C)),
                actions = {
                    Button(onClick = onSubscribeClick, colors = ButtonDefaults.buttonColors(containerColor = if (isSubscribed) Color(0xFF22C55E) else Color(0xFF9333EA))) {
                        Text(if (isSubscribed) "Активна" else "150 ₽/мес", color = Color.White)
                    }
                }
            )
        },
        containerColor = Color(0xFF0F0F13)
    ) { padding ->
        LazyColumn(modifier = Modifier.fillMaxSize().padding(padding), contentPadding = PaddingValues(16.dp), verticalArrangement = Arrangement.spacedBy(16.dp)) {
            items(movies) { movie ->
                Card(onClick = { onMovieClick(movie) }, colors = CardDefaults.cardColors(containerColor = Color(0xFF1A1A24)), modifier = Modifier.fillMaxWidth()) {
                    Row(modifier = Modifier.height(120.dp)) {
                        AsyncImage(model = movie.posterRes, contentDescription = null, contentScale = ContentScale.Crop, modifier = Modifier.width(90.dp).fillMaxHeight())
                        Column(modifier = Modifier.padding(12.dp)) {
                            Text(text = movie.genre, color = Color(0xFF9333EA), fontSize = 11.sp, fontWeight = FontWeight.Bold)
                            Text(text = movie.title, color = Color.White, fontSize = 16.sp, fontWeight = FontWeight.Bold)
                            Text(text = movie.description, color = Color.Gray, fontSize = 12.sp, maxLines = 2)
                        }
                    }
                }
            }
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun DetailScreen(movie: Movie, isSubscribed: Boolean, onBack: () -> Unit, onSelectEpisode: (Episode) -> Unit) {
    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text(movie.title, color = Color.White) },
                navigationIcon = { IconButton(onClick = onBack) { Icon(Icons.Default.ArrowBack, contentDescription = null, tint = Color.White) } },
                colors = TopAppBarDefaults.topAppBarColors(containerColor = Color(0xFF16161C))
            )
        },
        containerColor = Color(0xFF0F0F13)
    ) { padding ->
        LazyColumn(modifier = Modifier.fillMaxSize().padding(padding), contentPadding = PaddingValues(16.dp), verticalArrangement = Arrangement.spacedBy(12.dp)) {
            item {
                AsyncImage(model = movie.posterRes, contentDescription = null, contentScale = ContentScale.Crop, modifier = Modifier.fillMaxWidth().height(200.dp).clip(RoundedCornerShape(12.dp)))
                Spacer(modifier = Modifier.height(8.dp))
                Text(text = movie.description, color = Color.LightGray, fontSize = 14.sp)
                Spacer(modifier = Modifier.height(8.dp))
                Text(text = "Эпизоды", color = Color.White, fontSize = 18.sp, fontWeight = FontWeight.Bold)
            }
            items(movie.episodes) { ep ->
                val ok = ep.isFree || isSubscribed
                Card(onClick = { onSelectEpisode(ep) }, colors = CardDefaults.cardColors(containerColor = Color(0xFF1A1A24)), modifier = Modifier.fillMaxWidth()) {
                    Row(modifier = Modifier.padding(16.dp), verticalAlignment = Alignment.CenterVertically) {
                        Icon(imageVector = if (ok) Icons.Default.PlayArrow else Icons.Default.Lock, contentDescription = null, tint = if (ok) Color(0xFF22C55E) else Color(0xFF9333EA))
                        Spacer(modifier = Modifier.width(12.dp))
                        Text(text = ep.title, color = Color.White)
                    }
                }
            }
        }
    }
}

@Composable
fun PlayerScreen(episode: Episode, onBack: () -> Unit) {
    val context = LocalContext.current
    val activity = context as? Activity
    val configuration = LocalConfiguration.current
    val isLandscape = configuration.orientation == Configuration.ORIENTATION_LANDSCAPE

    val exoPlayer = remember {
        ExoPlayer.Builder(context).build().apply {
            setMediaItem(MediaItem.fromUri(episode.videoUrl))
            prepare()
            playWhenReady = true
        }
    }

    DisposableEffect(Unit) { onDispose { exoPlayer.release() } }

    Box(modifier = Modifier.fillMaxSize().background(Color.Black)) {
        AndroidView(factory = { PlayerView(it).apply { player = exoPlayer } }, modifier = Modifier.fillMaxSize())

        if (!isLandscape) {
            Row(modifier = Modifier.fillMaxWidth().padding(16.dp), horizontalArrangement = Arrangement.SpaceBetween) {
                IconButton(onClick = {
                    activity?.requestedOrientation = ActivityInfo.SCREEN_ORIENTATION_UNSPECIFIED
                    onBack()
                }, modifier = Modifier.background(Color(0x88000000), RoundedCornerShape(50.dp))) {
                    Icon(Icons.Default.ArrowBack, contentDescription = null, tint = Color.White)
                }
                IconButton(onClick = {
                    activity?.requestedOrientation = if (isLandscape) ActivityInfo.SCREEN_ORIENTATION_PORTRAIT else ActivityInfo.SCREEN_ORIENTATION_LANDSCAPE
                }, modifier = Modifier.background(Color(0x88000000), RoundedCornerShape(50.dp))) {
                    Icon(imageVector = if (isLandscape) Icons.Default.FullscreenExit else Icons.Default.Fullscreen, contentDescription = null, tint = Color.White)
                }
            }
        }
    }
}
""")

print("Project generated successfully!")
""")
