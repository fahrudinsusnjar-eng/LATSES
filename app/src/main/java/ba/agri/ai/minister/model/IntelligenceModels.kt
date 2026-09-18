package ba.agri.ai.minister.model

data class Claim(val text: String, val verified: Boolean? = null)
data class Source(val institution: String, val domain: String, val url: String, val authority: String, val verifiedAt: String? = null)
data class Evidence(val source: Source, val excerpt: String, val confidence: String)
data class VerificationResult(val claim: Claim, val status: String, val evidence: List<Evidence> = emptyList(), val uncertainty: String? = null)
data class FundingOpportunity(val name: String, val instrument: String, val provider: String, val amount: String? = null, val eligibility: String? = null)
data class FinancialFlow(val from: String, val through: String, val to: String, val instrument: String, val amount: String? = null)
data class TradeFlow(val origin: String, val destination: String, val commodity: String, val value: String? = null)
data class MigrationFlow(val origin: String, val destination: String, val people: String? = null, val reason: String? = null)
data class HealthEvent(val institution: String, val signal: String, val jurisdiction: String, val date: String)
data class ClimateSignal(val indicator: String, val location: String, val period: String, val signal: String)
data class DecisionBrief(val question: String, val facts: List<String>, val risks: List<String>, val options: List<String>, val sources: List<Source>)
