import flask
import settings

class Cal(flask.views.MethodView):
	def get(self, page='index'):
		return flask.render_template("cal.html", songs=songs)