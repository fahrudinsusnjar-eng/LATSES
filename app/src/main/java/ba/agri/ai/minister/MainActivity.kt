package ba.agri.ai.minister

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import ba.agri.ai.minister.data.OfficialSourceClient
import ba.agri.ai.minister.data.SourceCatalog
import ba.agri.ai.minister.ui.MinisterDashboard

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent { MinisterApp() }
    }
}

@Composable
fun MinisterApp() {
    var showInput by remember { mutableStateOf(false) }
    if (!showInput) {
        MinisterDashboard(onInput = { showInput = true })
    } else {
        var input by remember { mutableStateOf("") }
        var running by remember { mutableStateOf(false) }
        var result by remember { mutableStateOf<List<String>>(emptyList()) }

        MaterialTheme {
            Scaffold(topBar = { TopAppBar(title = { Text("TRAMP — Intelligent Input") }) }) { p ->
                Column(
                    Modifier.fillMaxSize().padding(p).padding(16.dp),
                    verticalArrangement = Arrangement.spacedBy(12.dp)
                ) {
                    Text("INPUT → CLAIMS → CONTEXT → SOURCES → EVIDENCE → LOGIC → FLOWS → DECISION")
                    OutlinedTextField(
                        value = input,
                        onValueChange = { input = it },
                        modifier = Modifier.fillMaxWidth(),
                        minLines = 5,
                        label = { Text("Pitanje / tvrdnja") }
                    )
                    Button(
                        enabled = input.isNotBlank() && !running,
                        onClick = {
                            running = true
                            result = listOf("Dohvaćam službene izvore…")
                            Thread {
                                val candidates = SourceCatalog.official.filter { source ->
                                    val q = input.lowercase()
                                    source.domains.any { q.contains(it.replace("-", " ")) || q.contains(it) } ||
                                        q.contains("ministar") || q.contains("program") || q.contains("subvenc")
                                }.ifEmpty { SourceCatalog.official.take(3) }

                                val fetched = candidates.map { source ->
                                    val r = OfficialSourceClient.fetch(source)
                                    when {
                                        r.error != null -> "${r.sourceId}: GREŠKA — ${r.error}"
                                        r.httpStatus in 200..299 -> "${r.sourceId}: HTTP ${r.httpStatus} — dohvaćeno ${r.retrievedAt}"
                                        else -> "${r.sourceId}: HTTP ${r.httpStatus} — nije potvrđeno"
                                    }
                                }
                                runOnUiThread {
                                    result = fetched + "NAPOMENA: dohvaćanje izvora nije isto što i potvrda tvrdnje."
                                    running = false
                                }
                            }.start()
                        },
                        modifier = Modifier.fillMaxWidth()
                    ) {
                        Text(if (running) "Dohvaćam…" else "Pokreni TRAMP analizu")
                    }

                    result.forEach { line ->
                        Card(Modifier.fillMaxWidth()) { Text(line, Modifier.padding(12.dp)) }
                    }

                    Text("TRAMP prikazuje rezultat dohvaćanja s datumom/vremenom. Tvrdnja ostaje NEPOTVRĐENA dok se dokaz iz dokumenta ne podudari s tvrdnjom.")
                    OutlinedButton(onClick = { showInput = false }) { Text("Nazad na dashboard") }
                }
            }
        }
    }
}
