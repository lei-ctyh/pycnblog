from core.util.log_util import log
from core.view.uploadWin import UploadWin

log.info("------------ cnblogmd项目开始启动 ------------")
win = UploadWin()
win.show()
log.info("------------ cnblogmd项目启动成功 ------------")
