package ba.agri.ai.minister.engine

import ba.agri.ai.minister.data.SourceCatalog
import ba.agri.ai.minister.model.*

data class EvidenceRecord(
    val sourceId:String,
    val institution:String,
    val url:String,
    val status:String,
    val checkedAt:String,
    val note:String
)

object EvidenceEngine {
    fun candidateSources(query:String):List<SourceRecordView> {
        val q=query.lowercase()
        return SourceCatalog.official
            .filter { it.domains.any { d -> q.contains(d) } || it.institution.lowercase().split(" ").any { w -> w.length>3 && q.contains(w) } }
            .map { SourceRecordView(it.id,it.institution,it.url,it.authority) }
    }
}
data class SourceRecordView(val id:String,val institution:String,val url:String,val authority:Int)
