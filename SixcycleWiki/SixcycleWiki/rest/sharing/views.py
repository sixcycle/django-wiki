from rest_framework.generics import GenericAPIView
from relationships.models import *
from SixcycleWiki.authentication.models import *
from SixcycleWiki.settings import WIKI_CAN_WRITE


class ShareView(GenericAPIView):

    def post(self, request, *args, **kwargs):
        '''
            users_list = [(<id>, read), (<id>, write)]
        
        '''
        users_list = request.data.get('users', None)
        groups_list = request.data.get('groups', None)
        orgs_list = request.data.get('organizations', None)
        article_id = request.data.get("article", None)
        article = Article.objects.get(id=article_id)

        if not WIKI_CAN_EDIT(request.user, article):
            return Response(status=403)

        for user in users_list:
            user_id = int(user[0])
            permission_type = user[1]
            try:
                user = User.objects.get(id=user_id)
                if permission_type == "read":
                    relation = UserReadArticle(user=user, article=article)
                    relation.save()
                if permission_type == "edit":
                    relation = UserEditArticle(user=user, article=article)
                    relation.save()
            except Exception as ex:
                pass

        for group in groups_list:
            group_id = int(group[0])
            permission_type = int(group[1])
            try:
                group = Group.objects.get(id=group_id)
                if permission_type == "read":
                    relation = GroupReadArticle(
                        group=group,
                        article=article
                    )
                    relation.save()
                if permission_type == "edit":
                    relation = GroupWriteArticle(
                        group=group,
                        article=article
                    )
                    relation.save()
            except Exception as ex:
                pass

        for org in orgs_list:
            org_id = int(org[0])
            permission_type = int(org[1])
            try:
                organization = Organization.objects.get(id=org_id)
                if permission_type == "read":
                    relation = OrganizationReadArticle(
                        group=group,
                        article=article
                    )
                    relation.save()
                if permission_type == "edit":
                    relation = OrganizationEditArticle(
                        group=group,
                        article=article
                    )
                    relation.save()
            except Exception as ex:
                pass

        return Response({"message": "success"})
