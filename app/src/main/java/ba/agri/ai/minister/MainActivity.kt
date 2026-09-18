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
import ba.agri.ai.minister.ui.MinisterDashboard

private data class Evidence(val title:String,val institution:String,val status:String,val note:String)

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) { super.onCreate(savedInstanceState); setContent { MinisterApp() } }
}

@Composable fun MinisterApp() {
    var showInput by remember { mutableStateOf(false) }
    if (!showInput) {
        MinisterDashboard(onInput = { showInput = true })
    } else {
        var input by remember { mutableStateOf("") }
        var result by remember { mutableStateOf<String?>(null) }
        MaterialTheme {
            Scaffold(topBar={ TopAppBar(title={ Text("TRAMP — Intelligent Input") }) }) { p ->
                Column(Modifier.fillMaxSize().padding(p).padding(16.dp), verticalArrangement=Arrangement.spacedBy(12.dp)) {
                    Text("INPUT → CLAIMS → CONTEXT → SOURCES → EVIDENCE → LOGIC → FLOWS → DECISION")
                    OutlinedTextField(value=input,onValueChange={input=it},modifier=Modifier.fillMaxWidth(),minLines=5,label={Text("Pitanje / tvrdnja")})
                    Button(enabled=input.isNotBlank(),onClick={result="Claim identified. Live verification requires the connected official-source backend."},modifier=Modifier.fillMaxWidth()){Text("Pokreni TRAMP analizu")}
                    result?.let { Card(Modifier.fillMaxWidth()){ Text(it,Modifier.padding(16.dp)) } }
                    Text("TRAMP ne izmišlja potvrđene izvore. Nepotvrđeno ostaje označeno kao nepotvrđeno.")
                    OutlinedButton(onClick={showInput=false}){Text("Nazad na dashboard")}
                }
            }
        }
    }
}
