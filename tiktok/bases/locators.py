# locators.py

# Search Form Locators
SEARCH_INPUT = 'input[data-e2e="search-user-input"]'
SEARCH_BUTTON = 'button[data-e2e="search-box-button"]'

# Tab Item Locator
USERS_TAB_ITEM_SELECTOR = 'div[data-e2e="tab-item"] div[role="tab"][aria-controls="tabs-0-panel-search_account"]'

# Profile container and profile link locators
PROFILE_CONTAINER = 'div[data-e2e="search-user-container"]'
PROFILE_LINK = 'a[href]'

# Comment scenario 1
NO_CONTENT = ".css-1ovqurc-PTitle.emuynwa1"
VIDEO_LINK = "//div[@data-e2e='user-post-item']//a[contains(@href, '/video')]"
NEXT_VIDEO = "//button[@data-e2e='arrow-right']"

# Comment Input and Send Button Locators
COMMENT_INPUT = "//div[@class='css-19hqadz-DivBottomCommentContainer e1mecfx04']//div[" \
                                 "@contenteditable='true']"
COMMENT_SEND_BUTTON = 'div[data-e2e="comment-post"]'

# Message scenario 1
# Follow Button Locators
FOLLOW_BUTTON = 'button[data-e2e="follow-button"]'

# Message Button Locators
PRIMARY_MESSAGE_BUTTON = '//button[@type="button" and contains(@class, "css-1btqthh-Button-StyledMessageButton") and ' \
                         'text()="Messages"]'
SECONDARY_MESSAGE_BUTTON = "//button[@class='TUXButton TUXButton--default TUXButton--medium TUXButton--secondary' and "\
                           "@aria-disabled='false' and @type='button' and @data-e2e='message-button']//div[" \
                           "@class='TUXButton-label' and text()='Message']"

# Message Input and Send Button Locators
MESSAGE_INPUT = 'div[aria-label="Send a message..."]'
MESSAGE_SEND_BUTTON = 'svg[data-e2e="message-send"]'

# Captcha
CAPTCHA_CONTAINER = "div.captcha_verify_container"
