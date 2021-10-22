require "bundler/setup"
require "pry"
require "dotenv"

Dotenv.load

require "./instagram_graph_api.rb"

BASE_URL = "https://graph.facebook.com/v11.0".freeze
BUSINESS_ACCOUNT_ID = ENV["BUSINESS_ACCOUNT_ID"].freeze
ACCESS_TOKEN = ENV["ACCESS_TOKEN"].freeze

iga = InstagramGrapghApi.new

username = "username"
business_acount_id = BUSINESS_ACCOUNT_ID
access_token = ACCESS_TOKEN

res = iga.fetch_user(username, business_acount_id, access_token)
p res.body
