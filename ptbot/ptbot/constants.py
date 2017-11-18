PT_API_LINK = "https://www.pivotaltracker.com/services/v5"

ACCOUNT_API_LINK = PT_API_LINK + "/accounts"
PROJECT_API_LINK = PT_API_LINK + "/projects"
PERSON_API_LINK = PT_API_LINK + "/my/people?project_id={project_id}"
STORY_API_LINK = PROJECT_API_LINK + "/{project_id}/stories"
