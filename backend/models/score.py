import mongoengine


class Score(mongoengine.Document):

    cub_account = mongoengine.StringField(required=True, unique=True)
    score = mongoengine.IntField(required=True)
    watchers_count = mongoengine.IntField()
    forks_count = mongoengine.IntField()
    stargazers_count = mongoengine.IntField()

    @classmethod
    def compute(cls, account):
        watchers = Repository.objects.filter(cub_account=account).sum('watchers_count')
        stargazers = Repository.objects.filter(cub_account=account).sum('stargazers_count')
        forks = Repository.objects.filter(cub_account=account).sum('forks_count')

        live_score =  watchers + stargazers + forks

        if Score.objects(cub_account=account):
            score = Score.objects.get(cub_account=account).modify(
                score=live_score, watchers_count=watchers,
                forks_count=forks, stargazers_count=stargazers)
        else:
            score = Score(cub_account=account, score=live_score,
                watchers_count=watchers, forks_count=forks,
                stargazers_count=stargazers).save()
        return score
