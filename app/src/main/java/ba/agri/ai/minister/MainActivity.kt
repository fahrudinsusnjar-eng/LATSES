package ba.agri.ai.minister

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp

private data class Evidence(val title:String,val institution:String,val status:String,val note:String)

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) { super.onCreate(savedInstanceState); setContent { MinisterApp() } }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable fun MinisterApp() {
    var input by remember { mutableStateOf("") }
    var result by remember { mutableStateOf<String?>(null) }
    val evidence = remember { listOf(
        Evidence("Official source registry","Configured source registry","READY","Every decisive claim must carry institution, date, version and URL."),
        Evidence("Claim verification","AGRI-AI verification engine","RULE","A statement is treated as a claim until verified."),
        Evidence("Decision brief","Ministerial decision support","DRAFT","Live official-source retrieval belongs to the backend layer.")
    ) }
    MaterialTheme {
        Scaffold(topBar={ TopAppBar(title={ Text("AGRI-AI Minister") }) }) { p ->
            LazyColumn(modifier=Modifier.fillMaxSize().padding(p).padding(16.dp), verticalArrangement=Arrangement.spacedBy(12.dp)) {
                item { Text("Intelligent input", style=MaterialTheme.typography.headlineSmall) }
                item { Text("Unesite tvrdnju, pitanje ili prijedlog. Sistem ga prvo razdvaja na provjerljive tvrdnje i određuje koji kontekst i izvori nedostaju.") }
                item { OutlinedTextField(value=input,onValueChange={input=it}, modifier=Modifier.fillMaxWidth(), minLines=4, label={Text("Pitanje / tvrdnja")}) }
                item { Button(enabled=input.isNotBlank(), onClick={result="INPUT → CLAIM CHECK → CONTEXT → OFFICIAL SOURCE CHECK → EVIDENCE → RESPONSE"}, modifier=Modifier.fillMaxWidth()) { Text("Pokreni provjeru") } }
                result?.let { r -> item { Card { Column(Modifier.padding(16.dp)) { Text("Kontrolni tok", style=MaterialTheme.typography.titleMedium); Spacer(Modifier.height(8.dp)); Text(r); Spacer(Modifier.height(8.dp)); Text("Ovaj početni build ne izmišlja činjenice niti simulira potvrđene izvore.", style=MaterialTheme.typography.bodySmall) } } } }
                item { Text("Kontrola izvora", style=MaterialTheme.typography.headlineSmall) }
                items(evidence) { ev -> Card { Column(Modifier.padding(16.dp)) { Text(ev.title, style=MaterialTheme.typography.titleMedium); Text(ev.institution); Text("Status: " + ev.status); Spacer(Modifier.height(4.dp)); Text(ev.note) } } }
                item { Text("Princip: činjenica bez provjerljivog izvora ostaje nepotvrđena tvrdnja.", style=MaterialTheme.typography.bodySmall) }
            }
        }
    }
}
