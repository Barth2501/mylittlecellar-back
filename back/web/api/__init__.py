from flask import Blueprint
from flask_restful import Api

from back.core import db

from .winery import Wineries, Area, Winery, Region, RegionsAreas
from .wine import Wines, Wine, WineVintage, WineOther, WineTrend, WinesFromWinery
from .recipe import ImportRecipes, RecipesToWines, ModifyIngRecipes, WinesToRecipes
from .me import MyCellar, Me, MyCellars, MyRegions, MyAreas, MyWineries, MyWines
from .cellar import CurrentCellar
from .statistics import RegionStat, AreaStat, VintageStat
from .test import Test

from .. import app

api_bp = Blueprint("api", __name__)
api = Api(api_bp)


@api_bp.before_request
def before_request():
    db.connect(reuse_if_open=True)
    pass


@api_bp.teardown_request
def after_request(exception=None):
    db.close()


api.add_resource(Wines, "/wines")
api.add_resource(Wine, "/wines/<int:wine_id>")
api.add_resource(WineVintage, "/wines/other_vintage/<int:wine_id>")
api.add_resource(WineOther, "/wines/other_wines/<int:wine_id>")
api.add_resource(WineTrend, "/wine_trend/<int:wine_id>")

api.add_resource(Wineries, "/wineries")
api.add_resource(Region, "/regions/<region_name>")
api.add_resource(Area, "/areas/<area_name>")
api.add_resource(Winery, "/wineries/<int:winery_id>")
api.add_resource(WinesFromWinery, "/wineries/<int:winery_id>/wines")
api.add_resource(RegionsAreas, "/regions_areas")

api.add_resource(ImportRecipes, "/import_recipes")
api.add_resource(ModifyIngRecipes, "/modify_ingredients_recipes")
api.add_resource(RecipesToWines, "/recipes_to_wines")
api.add_resource(WinesToRecipes, "/wines_to_recipes/<int:wine_id>")

api.add_resource(MyCellar, "/mycellar")
api.add_resource(MyCellars, "/mycellars")
api.add_resource(Me, "/me")
api.add_resource(MyRegions, "/myregions")
api.add_resource(MyAreas, "/myareas/<int:region_id>")
api.add_resource(MyWineries, "/mywineries/<int:area_id>")
api.add_resource(MyWines, "/mywines/<int:winery_id>")

api.add_resource(CurrentCellar, '/change_current_cellar')

api.add_resource(RegionStat, '/statistics/region_agg')
api.add_resource(AreaStat, '/statistics/area_agg/<region_name>')
api.add_resource(VintageStat, '/statistics/vintage_agg/<name>')

api.add_resource(Test, '/test')

app.register_blueprint(api_bp, url_prefix="/api/v1")