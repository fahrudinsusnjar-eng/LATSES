package ba.agri.ai.minister.engine
import ba.agri.ai.minister.model.*
enum class ClaimStatus { INPUT, NEEDS_CONTEXT, NEEDS_SOURCE, UNVERIFIED, VERIFIED }
data class ClaimCheck(val claim:Claim,val status:ClaimStatus,val requiredContext:List<String>,val requiredEvidence:List<String>)
object ClaimVerifier {
 fun inspect(claim:Claim):ClaimCheck {
  val text=claim.text.lowercase(); val context=mutableListOf<String>()
  if(listOf("eu","evrops","subvenc","fond","grant","program").any{text.contains(it)}) context+="jurisdiction / country / programme / eligibility year"
  if(listOf("najman","minimum","rok","uslov","iznos","kamata").any{text.contains(it)}) context+="measure / threshold / date / applicable version"
  if(context.isEmpty()) context+="jurisdiction / date / subject"
  return ClaimCheck(claim,ClaimStatus.NEEDS_SOURCE,context.distinct(),listOf("authoritative institution","current document or regulation","publication/effective date"))
 }
}