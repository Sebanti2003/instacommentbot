import threading
import logging
from flask import Blueprint, jsonify
from .bot import start_bot, stop_bot, bot_running, target_user_id
import pandas as pd
import os

logging.basicConfig(level=logging.INFO)

main_routes = Blueprint('main', __name__)

# Lock to manage bot state safely across threads
bot_lock = threading.Lock()

@main_routes.route('/start_bot', methods=['POST'])
def start_bot_route():
    try:
        with bot_lock:
            if bot_running:
                return jsonify({"message": "Bot is already running!"}), 400
            start_bot_thread = threading.Thread(target=start_bot)
            start_bot_thread.start()
        return jsonify({"message": "Bot started!"}), 200
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return jsonify({"message": f"Error: {str(e)}"}), 500

@main_routes.route('/stop_bot', methods=['POST'])
def stop_bot_route():
    try:
        with bot_lock:
            if not bot_running:
                return jsonify({"message": "Bot is not running!"}), 400
            stop_bot()
        return jsonify({"message": "Bot stopped!"}), 200
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return jsonify({"message": f"Error: {str(e)}"}), 500

@main_routes.route('/status', methods=['GET'])
def status_route():
    bot_status = "running" if bot_running else "idle"
    return jsonify({"status": bot_status}), 200

@main_routes.route('/liked_posts', methods=['GET'])
def liked_posts_route():
    try:
        likes_df = pd.read_csv('likes.csv')
        return jsonify(likes_df.to_dict(orient='records')), 200
    except FileNotFoundError:
        logging.warning("No liked posts found.")
        return jsonify({"message": "No liked posts found."}), 404

@main_routes.route('/commented_posts', methods=['GET'])
def commented_posts_route():
    try:
        commenting_df = pd.read_csv('commenting.csv')
        return jsonify(commenting_df.to_dict(orient='records')), 200
    except FileNotFoundError:
        logging.warning("No commented posts found.")
        return jsonify({"message": "No commented posts found."}), 404

@main_routes.route('/follow_status', methods=['GET'])
def follow_status_route():
    try:
        follow_df = pd.read_csv('follow.csv')
        if target_user_id in follow_df['user_id'].values:
            return jsonify({"message": "Following the target user."}), 200
        else:
            return jsonify({"message": "Not following the target user."}), 200
    except FileNotFoundError:
        logging.warning("No follow data found.")
        return jsonify({"message": "No follow data found."}), 404
