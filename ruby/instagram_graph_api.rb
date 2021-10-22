require "bundler/setup"
require "json"
require "faraday"
require "faraday_middleware"

# Instagram Grapg APIを叩くためのクラス
class InstagramGrapghApi
  def initialize
    @client = Faraday.new(url: BASE_URL) do |config|
      config.request :url_encoded
      config.response :json
      config.response :raise_error
      config.adapter Faraday.default_adapter
    end
  end

  # ユーザーの情報を取得
  def fetch_user(username, business_acount_id, access_token)
    fields = <<~FIELDS
      business_discovery.username(#{username}){
        id,
        username,
        biography,
        profile_picture_url,
        follows_count,
        followers_count,
        media_count
      }
    FIELDS

    @client.get("#{business_acount_id}", {
      fields: fields.gsub(/\r\n|\r|\n|\s|\t/, ""),
      access_token: access_token,
    })
  end

  # ユーザーのインサイトを取得
  def fetch_user_insght(username, business_acount_id, access_token, period = "day", since = nil)
    @client.get("#{business_acount_id}/insights?", {
      metric: %w[
        impressions
        reach
        follower_count
        profile_views
        email_contacts
        get_directions_clicks
        phone_call_clicks
        text_message_clicks
        website_clicks
      ].join(","),
      period: period,
      since: since,
      access_token: access_token,
    })
  end

  # メディアの情報を取得
  def fetch_media(username, business_acount_id, access_token, limit = 25, next_token = nil)
    fields = <<~FIELDS
      business_discovery.username(#{username}){
        media.limit(#{limit})%s{
          id,
          comments_count,
          caption,
          like_count,
          media_type,
          media_url,
          permalink,
          timestamp
        }
      }
    FIELDS

    fields = fields % (next_token ? ".after(#{next_token})" : "")
    @client.get("#{business_acount_id}", {
      fields: fields.gsub(/\r\n|\r|\n|\s|\t/, ""),
      access_token: access_token
    })
  end

  # メディアのインサイトを取得
  def fetch_media_insght(media_id, access_token)
    @client.get("/#{media_id}/insights", {
      metric: %w[
        engagement
        reach
        impressions
        saved
      ].join(","),
      access_token: access_token
    })
  end
end
