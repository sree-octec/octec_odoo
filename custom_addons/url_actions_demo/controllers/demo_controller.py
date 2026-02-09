from odoo import http
from odoo.http import request
from odoo.modules.module import get_module_resource

class UrlDemoController(http.Controller):
  
  @http.route("/demo_url_actions/download/sample", type="http", auth="user")
  def download_file(self, **kw):
    path = get_module_resource('url_actions_demo','static/src/pdf','sample.pdf')
    return http.send_file(path, filename="sample.pdf")