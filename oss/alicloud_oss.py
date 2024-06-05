import oss2
from oss2.credentials import EnvironmentVariableCredentialsProvider
from itertools import islice

endpoint = 'oss-cn-shanghai.aliyuncs.com'
# 从环境变量中获取访问凭证。运行本代码示例之前，请确保已设置环境变量OSS_ACCESS_KEY_ID和OSS_ACCESS_KEY_SECRET。
auth = oss2.ProviderAuth(EnvironmentVariableCredentialsProvider())
bucket = oss2.Bucket(auth, endpoint, 'husbucket')

def read_bucket():
    for b in islice(oss2.ObjectIterator(bucket), 10):
        print(b.key)
    
def upload_file():
    
    bucket.put_object_from_file('', 'yourLocalFile')
