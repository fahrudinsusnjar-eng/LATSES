package ba.agri.ai.minister.data
data class OfficialSource(val id:String,val institution:String,val scope:String,val domain:String,val baseUrl:String)
object OfficialSourceRegistry {
 val sources=listOf(
  OfficialSource("EU","European Union","EU","Funding / Agriculture / Law","https://european-union.europa.eu/"),
  OfficialSource("FAO","Food and Agriculture Organization","Global","Agriculture / Food","https://www.fao.org/"),
  OfficialSource("IFAD","International Fund for Agricultural Development","Global","Rural Finance","https://www.ifad.org/"),
  OfficialSource("EBRD","European Bank for Reconstruction and Development","Europe / Central Asia","Finance / Investment","https://www.ebrd.com/"),
  OfficialSource("EIB","European Investment Bank","Europe","Finance / Investment","https://www.eib.org/"),
  OfficialSource("WHO","World Health Organization","Global","Health","https://www.who.int/"),
  OfficialSource("IOM","International Organization for Migration","Global","Migration","https://www.iom.int/"),
  OfficialSource("WORLD_BANK","World Bank","Global","Development / Finance","https://www.worldbank.org/"),
  OfficialSource("GEF","Global Environment Facility","Global","Environment / Finance","https://www.thegef.org/"),
  OfficialSource("GCF","Green Climate Fund","Global","Climate / Finance","https://www.greenclimate.fund/")
 )
}