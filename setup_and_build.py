import os

def create_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

# 1. Gradle Project Files
create_file("build.gradle", """
buildscript {
    repositories {
        google()
        mavenCentral()
    }
    dependencies {
        classpath 'com.android.tools.build:gradle:8.2.0'
        classpath "org.jetbrains.kotlin:kotlin-gradle-plugin:1.9.20"
    }
}
allprojects {
    repositories {
        google()
        mavenCentral()
    }
}
""")

create_file("settings.gradle", """
pluginManagement {
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
include ':app'
""")

create_file("app/build.gradle", """
plugins {
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
        testInstrumentationRunner "androidx.test.runner.AndroidJUnitRunner"
        vectorDrawables {
            useSupportLibrary true
        }
    }

    buildTypes {
        release {
            minifyEnabled false
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
        }
    }
    compileOptions {
        sourceCompatibility JavaVersion.VERSION_17
        targetCompatibility JavaVersion.VERSION_17
    }
    kotlinOptions {
        jvmTarget = '17'
    }
    buildFeatures {
        compose true
    }
    composeOptions {
        kotlinCompilerExtensionVersion '1.5.4'
    }
    packagingOptions {
        resources {
            excludes += '/META-INF/{AL2.0,LGPL2.1}'
        }
    }
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
    
    // Media3 ExoPlayer для видео и HLS
    implementation 'androidx.media3:media3-exoplayer:1.2.0'
    implementation 'androidx.media3:media3-exoplayer-hls:1.2.0'
    implementation 'androidx.media3:media3-ui:1.2.0'
}
""")

create_file("app/src/main/AndroidManifest.xml", """
<?xml version="1.0" encoding="utf-8"?>
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

create_file("app/src/main/res/values/themes.xml", """
<resources>
    <style name="Theme.KinoClub" parent="Theme.Material3.Dark.NoActionBar">
        <item name="android:statusBarColor">@android:color/black</item>
        <item name="android:navigationBarColor">@android:color/black</item>
    </style>
</resources>
""")

# 2. Kotlin Code (Models & Repository)
create_file("app/src/main/java/com/kinoclub/app/Model.kt", """
package com.kinoclub.app

data class Episode(
    val id: Int,
    val title: String,
    val videoUrl: String,
    val isFree: Boolean
)

data class Movie(
    val id: Int,
    val title: String,
    val type: String, // "Фильм" или "Сериал"
    val author: String,
    val description: String,
    val posterRes: String,
    val genre: String,
    val episodes: List<Episode>
)

object MockRepository {
    val movies = listOf(
        Movie(
            id = 1,
            title = "Ночной дрифт",
            type = "Фильм",
            author = "StudioDrift",
            description = "Авторский фильм о ночных заездах, тюнинге и уличной культуре. Доступен бесплатно для ознакомления.",
            genre = "Экшн / Авто",
            posterRes = "https://images.unsplash.com/photo-1503376780353-7e6692767b70?w=600",
            episodes = listOf(
                Episode(1, "Полнометражный фильм", "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4", true)
            )
        ),
        Movie(
            id = 2,
            title = "Тайны Сибири",
            type = "Сериал",
            author = "SiberiaFilm",
            description = "Независимый детективный сериал об экспедиции в глухие таежные места. 1-я серия бесплатно, продолжение — по подписке 150 ₽/мес.",
            genre = "Детектив / Триллер",
            posterRes = "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=600",
            episodes = listOf(
                Episode(1, "Серия 1: Начало пути", "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4", true),
                Episode(2, "Серия 2: Ледяной след", "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4", false),
                Episode(3, "Серия 3: Заброшенный кордон", "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerEscapes.mp4", false)
            )
        ),
        Movie(
            id = 3,
            title = "Гараж мечты",
            type = "Фильм",
            author = "AutoMasters",
            description = "Полномасштабный авторский проект о восстановлении редких классических автомобилей сбоку до конвейера.",
            genre = "Документальный",
            posterRes = "https://images.unsplash.com/photo-1486006920555-c77dce18193b?w=600",
            episodes = listOf(
                Episode(1, "Часть 1: Разборка и дефектовка", "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/TearsOfSteel.mp4", false)
            )
        )
    )
}
""")

# 3. Main Activity с полным UI, плеером, качеством, озвучкой и полноэкранным режимом
create_file("app/src/main/java/com/kinoclub/app/MainActivity.kt", """
package com.kinoclub.app

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
import androidx.media3.common.TrackSelectionOverride
import androidx.media3.common.C
import androidx.media3.exoplayer.ExoPlayer
import androidx.media3.ui.PlayerView
import coil.compose.AsyncImage

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            Surface(
                modifier = Modifier.fillMaxSize(),
                color = Color(0xFF0F0F13)
            ) {
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

    if (activeEpisode != null && selectedMovie != null) {
        PlayerScreen(
            movie = selectedMovie!!,
            episode = activeEpisode!!,
            onBack = { activeEpisode = null }
        )
    } else if (selectedMovie != null) {
        DetailScreen(
            movie = selectedMovie!!,
            isSubscribed = isSubscribed,
            onBack = { selectedMovie = null },
            onSelectEpisode = { ep ->
                if (ep.isFree || isSubscribed) {
                    activeEpisode = ep
                } else {
                    showPaywall = true
                }
            }
        )
    } else {
        HomeScreen(
            movies = MockRepository.movies,
            isSubscribed = isSubscribed,
            onMovieClick = { selectedMovie = it },
            onSubscribeClick = { showPaywall = true }
        )
    }

    if (showPaywall) {
        PaywallDialog(
            onDismiss = { showPaywall = false },
            onSuccess = {
                isSubscribed = true
                showPaywall = false
            }
        )
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun HomeScreen(
    movies: List<Movie>,
    isSubscribed: Boolean,
    onMovieClick: (Movie) -> Unit,
    onSubscribeClick: () -> Unit
) {
    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("KINO-CLUB", fontWeight = FontWeight.Bold, color = Color.White) },
                colors = TopAppBarDefaults.topAppBarColors(containerColor = Color(0xFF16161C)),
                actions = {
                    Button(
                        onClick = onSubscribeClick,
                        colors = ButtonDefaults.buttonColors(
                            containerColor = if (isSubscribed) Color(0xFF22C55E) else Color(0xFF9333EA)
                        ),
                        shape = RoundedCornerShape(20.dp),
                        modifier = Modifier.padding(end = 12.dp)
                    ) {
                        Icon(
                            imageVector = if (isSubscribed) Icons.Default.Check else Icons.Default.Star,
                            contentDescription = null,
                            modifier = Modifier.size(16.dp),
                            tint = Color.White
                        )
                        Spacer(modifier = Modifier.width(6.dp))
                        Text(
                            text = if (isSubscribed) "Подписка активна" else "150 ₽/мес",
                            color = Color.White,
                            fontSize = 13.sp
                        )
                    }
                }
            )
        },
        containerColor = Color(0xFF0F0F13)
    ) { padding ->
        LazyColumn(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding),
            contentPadding = PaddingValues(16.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            item {
                Text(
                    text = "Премьеры и авторское кино",
                    color = Color.Gray,
                    fontSize = 14.sp,
                    modifier = Modifier.padding(bottom = 4.dp)
                )
            }
            items(movies) { movie ->
                MovieCard(movie = movie, onClick = { onMovieClick(movie) })
            }
        }
    }
}

@Composable
fun MovieCard(movie: Movie, onClick: () -> Unit) {
    Card(
        onClick = onClick,
        shape = RoundedCornerShape(16.dp),
        colors = CardDefaults.cardColors(containerColor = Color(0xFF1A1A24)),
        elevation = CardDefaults.cardElevation(defaultElevation = 6.dp),
        modifier = Modifier.fillMaxWidth()
    ) {
        Row(modifier = Modifier.height(140.dp)) {
            AsyncImage(
                model = movie.posterRes,
                contentDescription = null,
                contentScale = ContentScale.Crop,
                modifier = Modifier
                    .width(100.dp)
                    .fillMaxHeight()
            )
            Column(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(12.dp),
                verticalArrangement = Arrangement.SpaceBetween
            ) {
                Column {
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween
                    ) {
                        Text(
                            text = movie.genre,
                            color = Color(0xFF9333EA),
                            fontSize = 11.sp,
                            fontWeight = FontWeight.Bold
                        )
                        Surface(
                            shape = RoundedCornerShape(4.dp),
                            color = Color(0xFF2A2A38)
                        ) {
                            Text(
                                text = movie.type,
                                color = Color.LightGray,
                                fontSize = 10.sp,
                                modifier = Modifier.padding(horizontal = 6.dp, vertical = 2.dp)
                            )
                        }
                    }
                    Spacer(modifier = Modifier.height(4.dp))
                    Text(
                        text = movie.title,
                        color = Color.White,
                        fontSize = 18.sp,
                        fontWeight = FontWeight.Bold
                    )
                    Text(
                        text = "Автор: ${movie.author}",
                        color = Color.Gray,
                        fontSize = 12.sp
                    )
                }
                Text(
                    text = movie.description,
                    color = Color.LightGray,
                    fontSize = 12.sp,
                    maxLines = 2
                )
            }
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun DetailScreen(
    movie: Movie,
    isSubscribed: Boolean,
    onBack: () -> Unit,
    onSelectEpisode: (Episode) -> Unit
) {
    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text(movie.title, color = Color.White) },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.Default.ArrowBack, contentDescription = "Назад", tint = Color.White)
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(containerColor = Color(0xFF16161C))
            )
        },
        containerColor = Color(0xFF0F0F13)
    ) { padding ->
        LazyColumn(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding),
            contentPadding = PaddingValues(16.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            item {
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(220.dp)
                        .clip(RoundedCornerShape(16.dp))
                ) {
                    AsyncImage(
                        model = movie.posterRes,
                        contentDescription = null,
                        contentScale = ContentScale.Crop,
                        modifier = Modifier.fillMaxSize()
                    )
                    Box(
                        modifier = Modifier
                            .fillMaxSize()
                            .background(
                                Brush.verticalGradient(
                                    colors = listOf(Color.Transparent, Color(0xFF0F0F13)),
                                    startY = 100f
                                )
                            )
                    )
                }
            }
            item {
                Text(text = movie.genre, color = Color(0xFF9333EA), fontSize = 13.sp, fontWeight = FontWeight.Bold)
                Text(text = movie.title, color = Color.White, fontSize = 24.sp, fontWeight = FontWeight.Bold)
                Text(text = "Режиссер / Автор: ${movie.author}", color = Color.Gray, fontSize = 13.sp)
                Spacer(modifier = Modifier.height(8.dp))
                Text(text = movie.description, color = Color.LightGray, fontSize = 14.sp)
                Spacer(modifier = Modifier.height(16.dp))
                Text(text = "Эпизоды и материалы", color = Color.White, fontSize = 18.sp, fontWeight = FontWeight.Bold)
            }
            items(movie.episodes) { episode ->
                val accessible = episode.isFree || isSubscribed
                Card(
                    onClick = { onSelectEpisode(episode) },
                    colors = CardDefaults.cardColors(containerColor = Color(0xFF1A1A24)),
                    shape = RoundedCornerShape(12.dp),
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(16.dp),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.weight(1f)) {
                            Icon(
                                imageVector = if (accessible) Icons.Default.PlayArrow else Icons.Default.Lock,
                                contentDescription = null,
                                tint = if (accessible) Color(0xFF22C55E) else Color(0xFF9333EA),
                                modifier = Modifier.size(28.dp)
                            )
                            Spacer(modifier = Modifier.width(12.dp))
                            Column {
                                Text(text = episode.title, color = Color.White, fontSize = 15.sp, fontWeight = FontWeight.Medium)
                                Text(
                                    text = if (episode.isFree) "Бесплатный ознакомительный контент" else "Требуется подписка (150 ₽/мес)",
                                    color = Color.Gray,
                                    fontSize = 12.sp
                                )
                            }
                        }
                    }
                }
            }
        }
    }
}

@Composable
fun PlayerScreen(
    movie: Movie,
    episode: Episode,
    onBack: () -> Unit
) {
    val context = LocalContext.current
    val activity = context as? Activity
    val configuration = LocalConfiguration.current
    val isLandscape = configuration.orientation == Configuration.ORIENTATION_LANDSCAPE

    val exoPlayer = remember {
        ExoPlayer.Builder(context).build(
