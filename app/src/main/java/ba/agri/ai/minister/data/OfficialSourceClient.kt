package ba.agri.ai.minister.data

import java.net.HttpURLConnection
import java.net.URI
import java.time.Instant

data class SourceFetchResult(
    val sourceId: String,
    val url: String,
    val httpStatus: Int?,
    val contentType: String?,
    val retrievedAt: String,
    val bodyPreview: String?,
    val error: String?
)

object OfficialSourceClient {
    fun fetch(source: SourceRecord): SourceFetchResult {
        return try {
            val connection = URI(source.url).toURL().openConnection() as HttpURLConnection
            connection.connectTimeout = 8000
            connection.readTimeout = 10000
            connection.instanceFollowRedirects = true
            connection.requestMethod = "GET"
            connection.setRequestProperty("User-Agent", "TRAMP/0.1")
            val status = connection.responseCode
            val stream = if (status in 200..399) connection.inputStream else connection.errorStream
            val body = stream?.bufferedReader()?.use { it.readText() } ?: ""
            SourceFetchResult(source.id, source.url, status, connection.contentType, Instant.now().toString(), body.replace(Regex("\\s+"), " ").take(1200), null)
        } catch (e: Exception) {
            SourceFetchResult(source.id, source.url, null, null, Instant.now().toString(), null, e.message ?: e.javaClass.simpleName)
        }
    }
}