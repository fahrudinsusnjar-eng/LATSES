package ba.agri.ai.minister.ui

import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import ba.agri.ai.minister.engine.IntelligencePipeline

@Composable
fun MinisterDashboard(onInput: () -> Unit) {
    Column(Modifier.padding(20.dp), verticalArrangement = Arrangement.spacedBy(12.dp)) {
        Text("TRAMP", style = MaterialTheme.typography.headlineLarge)
        Text("Strategic intelligence for agricultural and public-sector decisions.")
        Button(onClick = onInput) { Text("Intelligent Input") }
        IntelligencePipeline.supportedDomains().forEach { domain ->
            ElevatedCard(Modifier.fillMaxWidth()) {
                Text(domain, Modifier.padding(16.dp))
            }
        }
    }
}
