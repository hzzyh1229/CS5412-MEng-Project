from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from azure.cosmos import CosmosClient
from datetime import datetime, date
import requests
API_BASE = "https://cs5412cloudjobboard.azurewebsites.net/"

user_center_bp = Blueprint('user_center_bp', __name__, template_folder='templates')
URL = "https://playground2.documents.azure.com:443/"
KEY = "v2V0lRtUsNNYEckQfGlvrAOFGjxhxGkKDSge2CXMccGdKB2lSxXmmfMtyuUcjeWuBCaCTntdeGf0QnFB9C8xuQ=="
client = CosmosClient(URL, credential=KEY)
DATABASE_NAME = 'Job Board'
database = client.get_database_client(DATABASE_NAME)

CONTAINER_NAME = 'Applications'
container = database.get_container_client(CONTAINER_NAME)

@user_center_bp.route('/user_center', methods=['GET', 'POST'])
def user_center():
  if current_user.is_authenticated:
    # print(current_user.get_username())
    return render_template("user_center.html")
  return redirect(url_for('login_bp.login'))
  

@user_center_bp.route('/user_center/profile', methods=['GET', 'POST'])
@login_required
def profile():
  username = current_user.get_username()['email']
  # print(username)
  nickname = current_user.get_nickname()
  # print(nickname)
  return render_template("profile.html", email=username, nickname=nickname)

@user_center_bp.route('/user_center/applications', methods=['GET', 'POST'])
@login_required
def applications():
  if request.method == "POST":
    new_status = ""
    update_type = -1;
    if "update-OA/VO" in request.form.keys():
      new_status = request.form["update-OA/VO"]
      update_type = 0;
    if "update-offer" in request.form.keys():
      new_status = request.form["update-offer"]
      update_type = 1;
    if "update-rejected" in request.form.keys():
      new_status = request.form["update-rejected"]
      update_type = 2;
    if "delete" in request.form.keys():
      new_status = request.form["delete"]
      update_type = 3;
    info_lst = new_status.split("+")
    if (len(info_lst) == 2):
      job_id = info_lst[0]
      new_status = info_lst[1]
      cur_date = datetime.today().strftime('%Y/%m/%d')
      # delete repetitive data entries and get old info
      for item in container.query_items(
        query='SELECT * FROM Applications WHERE Applications.job_id = @id AND Applications.email = @email',
        parameters=[dict(name="@id", value=job_id), dict(name='@email', value=current_user.get_username()['email'])],
        enable_cross_partition_query=True):
      # for item in requests.get(API_BASE + f"/applications/{job_id}/null/any"):
          title_company = item["title_company"] if "title_company" in item else "N/A"
          apply_date = item["apply_date"] if "apply_date" in item else "N/A"
          oa_vo_date = item["oa_vo_date"] if "oa_vo_date" in item else "N/A"
          offer_date = item["offer_date"] if "offer_date" in item else "N/A"
          reject_date = item["reject_date"] if "reject_date" in item else "N/A"
          container.delete_item(item, partition_key=current_user.get_username()['email'])
      if (update_type != 3):
        container.upsert_item({"email":current_user.get_username()['email'], "job_id": job_id, "title_company": title_company,
        "status": new_status, "apply_date": apply_date, "oa_vo_date": cur_date if update_type == 0 else oa_vo_date, 
        "offer_date": cur_date if update_type == 1 else offer_date,
        "reject_date": cur_date if update_type == 2 else reject_date})
  # get application_info after update
  application_info = list(container.query_items(
        query='SELECT * FROM Applications WHERE Applications.email = @email',
            parameters=[dict(name="@email", value=current_user.get_username()['email'])], 
            enable_cross_partition_query=True))
  application_info = sorted(application_info, key=lambda d: d['job_id'])
  # application_info = requests.get(API_BASE + f"applications/null/{current_user.get_username()['email']}/any")
  return render_template("applications.html", applications = application_info)

@user_center_bp.route('/user_center/analysis', methods=['GET', 'POST'])
@login_required
def analysis():
  application_info = list(container.query_items(
        query='SELECT * FROM Applications WHERE Applications.email = @email',
            parameters=[dict(name="@email", value=current_user.get_username()['email'])], 
            enable_cross_partition_query=True))
  total_num = len(application_info)
  total_OA_VO = 0
  days_OA_VO = 0
  total_offer = 0
  days_offer = 0
  total_reject = 0
  days_reject = 0
  for item in application_info:
    apply_date_list = item["apply_date"].split("/")
    d0 = date(int(apply_date_list[0]), int(apply_date_list[1]), int(apply_date_list[2]))
    if (item["oa_vo_date"] != "N/A"):
      total_OA_VO += 1
      oa_vo_date_list = item["oa_vo_date"].split("/")
      d1 = date(int(oa_vo_date_list[0]), int(oa_vo_date_list[1]), int(oa_vo_date_list[2]))
      days_OA_VO += (d1 - d0).days
    if (item["offer_date"] != "N/A"):
      total_offer += 1
      offer_date_list = item["offer_date"].split("/")
      d2 = date(int(offer_date_list[0]), int(offer_date_list[1]), int(offer_date_list[2]))
      days_offer += (d2 - d0).days
    if (item["reject_date"] != "N/A"):
      total_reject += 1
      reject_date_list = item["reject_date"].split("/")
      d3 = date(int(reject_date_list[0]), int(reject_date_list[1]), int(reject_date_list[2]))
      days_reject += (d3 - d0).days
  analysis_info = {
    "OA_VO_rate": total_OA_VO / total_num, "OA_VO_speed": str(days_OA_VO / total_OA_VO) + " days", 
    "offer_rate": total_offer / total_num, "offer_speed": str(days_offer / total_offer) + " days", 
    "reject_rate": total_reject / total_num, "reject_speed": str(days_reject / total_reject) + " days"
  }
  return render_template("analysis.html", analysis = analysis_info)

@user_center_bp.route('/logout')
@login_required
def logout():
    """
    return the logout page
    """
    logout_user()
    flash('Log out successfully.')
    return redirect(url_for('home.home'))