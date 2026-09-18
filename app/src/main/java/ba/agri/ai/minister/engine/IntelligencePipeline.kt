package ba.agri.ai.minister.engine

import ba.agri.ai.minister.model.*

object IntelligencePipeline {
    fun classify(input: String): List<Claim> =
        input.split(".").mapNotNull { it.trim().takeIf(String::isNotEmpty) }.map { Claim(it) }

    fun workflow(): List<String> = listOf(
        "INPUT","CLAIMS","CONTEXT","OFFICIAL SOURCES","EVIDENCE",
        "LOGIC CHECK","FLOW ANALYSIS","DECISION BRIEF"
    )

    fun supportedDomains(): List<String> = listOf(
        "Agriculture","Funding","Banking & Capital","Trade & Supply Chains",
        "Migration","WHO / Health","Climate & Natural Resources",
        "Law & Regulation","Investment & Due Diligence","Statistics"
    )
}
