package ba.agri.ai.minister.data

data class SourceRecord(
    val id:String,
    val institution:String,
    val url:String,
    val authority:Int,
    val domains:List<String>
)

object SourceCatalog {
    val official=listOf(
        SourceRecord("EU","European Union","https://european-union.europa.eu/",5,listOf("law","funding","agriculture")),
        SourceRecord("FAO","Food and Agriculture Organization","https://www.fao.org/",5,listOf("agriculture","food","statistics")),
        SourceRecord("WHO","World Health Organization","https://www.who.int/",5,listOf("health")),
        SourceRecord("IOM","International Organization for Migration","https://www.iom.int/",5,listOf("migration")),
        SourceRecord("EBRD","European Bank for Reconstruction and Development","https://www.ebrd.com/",5,listOf("finance","investment")),
        SourceRecord("EIB","European Investment Bank","https://www.eib.org/",5,listOf("finance","investment")),
        SourceRecord("WORLD_BANK","World Bank","https://www.worldbank.org/",5,listOf("development","finance")),
        SourceRecord("IFAD","International Fund for Agricultural Development","https://www.ifad.org/",5,listOf("agriculture","rural-finance"))
    )
}