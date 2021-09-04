import json
from instagram_graph_api import InstagramGraphApi

def run():
    instagram_graph_api = InstagramGraphApi()
    username = 'hogefugapiyo' # 情報を取得したいInstagramアカウントのユーザー名

    # name: 表示名、username:ユーザー名、biography: プロフィール文、follows_count: フォロー数、followers_count: フォロワー数、media_count: メディア数
    user = instagram_graph_api.get_user(username, 'name,username,biography,follows_count,followers_count,media_count')
    
    # impressions: ユーザーのメディアが閲覧された合計回数、reach: ユーザーのメディアを1つ以上閲覧したユニークユーザーの合計数、profile_views: ユーザーのプロフィールが閲覧された合計回数
    user_insight = instagram_graph_api.get_user_insight('impressions,reach,profile_views', 'day')
    user_info = {
        'user': user,
        'insight': user_insight
    }

    # timestamp: タイムスタンプ、caption: 本文、like_count: いいね数、comments_count: コメント数
    media = instagram_graph_api.get_media(username, 'timestamp,caption,like_count,comments_count')
    media_info = []
    
    for media in media:
        # engagement: いいね数・コメント数・保存数の合計、reach: メディアを閲覧したユニークユーザーの合計数、impressions: メディアが閲覧された合計回数、saved: 保存数
        media_insight = instagram_graph_api.get_media_insight(media['id'], 'engagement,reach,impressions,saved')

        media_info.append({
            'media': media,
            'insight': media_insight
        })

    print("【ユーザー情報】\n")
    print(json.dumps(user_info, ensure_ascii = False))

    print("\n------------------------\n")

    print("【メディア情報】\n")
    print(json.dumps(media_info, ensure_ascii = False))

if __name__ == '__main__':
    run()
