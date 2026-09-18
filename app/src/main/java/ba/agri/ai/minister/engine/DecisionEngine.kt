package ba.agri.ai.minister.engine

import ba.agri.ai.minister.model.*

data class DecisionOutput(
    val claims:List<Claim>,
    val sources:List<String>,
    val state:String,
    val warning:String
)

object DecisionEngine {
    fun analyze(input:String):DecisionOutput {
        val claims=IntelligencePipeline.classify(input)
        val sources=EvidenceEngine.candidateSources(input).map { it.institution }
        return DecisionOutput(
            claims=claims,
            sources=sources,
            state=if(sources.isEmpty()) "NEEDS_SOURCE" else "NEEDS_LIVE_VERIFICATION",
            warning="Kandidati izvora nisu dokaz. Live dokument mora biti dohvaćen i provjeren prije zaključka."
        )
    }
}