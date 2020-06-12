from Logger import main as log_class
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest
from soccerUI.HttpHandlers.mongoDB_API import mongo_API as MongoApi

class HttpHandler:
    """
    description
    """
    def __init__(self):
        self.logger = log_class.setup_logger('server-http-handler.log')
        self.mongoApi = MongoApi()
#        self.looger.info("HttpHandler,__init__ : using mongoAPI with the ip :".format(self.mongoApi.ip, self.mongoApi.port))


    @csrf_exempt
    def insert_to_db(self, request):
        self.logger.info("insert_to_db, receive request : {}".format(request))
        if request.method == 'POST':
            league = request.POST.get('TournamentName')
            season = request.POST.get('SeasonName')
            self.logger.info(request.POST)
            self.logger.info("league : {} season : {}".format(league, season))
            self.mongoApi.insert_json_object(dict(request.POST.copy()), 'results', league+season)
            return HttpResponse()
        else:
            return HttpResponseBadRequest

    @csrf_exempt
    def get_collection(self, request):
        self.logger.info("get_collection, receive request : {}".format(request))
        if request.method == 'POST':
            league = request.POST.get('TournamentName')
            season = request.POST.get('SeasonName')
            db_name = request.POST.get('db_name')
            filter = request.POST.get('filter')
            self.logger.info(request.POST)
            self.logger.info("league : {} season : {}".format(league, season))
            res_cursor = self.mongoApi.get_collection(db_name=db_name,
                                                      collection=league+season,
                                                      filter=filter)

            reslist = "["
            for json in res_cursor:
                reslist += "{"
                reslist += str(json)
                reslist += "},"

            del reslist[respone.__len__()-1]
            reslist += "]"
            return HttpResponse(reslist)
        else:
            return HttpResponseBadRequest



