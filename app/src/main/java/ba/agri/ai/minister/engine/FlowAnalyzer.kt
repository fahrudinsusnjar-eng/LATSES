package ba.agri.ai.minister.engine
import ba.agri.ai.minister.model.*
data class FlowSnapshot(val financial:List<FinancialFlow> = emptyList(),val trade:List<TradeFlow> = emptyList(),val migration:List<MigrationFlow> = emptyList(),val health:List<HealthEvent> = emptyList(),val climate:List<ClimateSignal> = emptyList())
object FlowAnalyzer { fun dimensions()=listOf("Money","Banking & Capital","Investment","Production","Jobs","Migration","Income","Taxes","Health","Food","Trade","Climate") }