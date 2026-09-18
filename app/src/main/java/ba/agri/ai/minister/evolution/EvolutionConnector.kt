package ba.agri.ai.minister.evolution

/**
 * Narrow extension point for future TRAMP evolution.
 *
 * This connector is intentionally read-only. It does not expose write,
 * delete, commit, or mutation operations against LATCES or any other
 * development repository.
 */
interface EvolutionConnector {
    fun status(): EvolutionStatus
}

data class EvolutionStatus(
    val enabled: Boolean = false,
    val mode: String = "READ_ONLY",
    val note: String = "Future evolution connector only; no repository mutation."
)
