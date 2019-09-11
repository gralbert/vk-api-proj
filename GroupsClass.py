import requests
from vklancer import api
import json
from concurrent.futures import ThreadPoolExecutor
from queue import Queue
import threading

MY_TOKEN = '0688a8b20688a8b20688a8b22206e05b9e' \
               '006880688a8b25afd5bad0eb94304d8447dc4'

vk = api.API(MY_TOKEN)

class Group:
    def __init__(self, uid, max_users):
        self.uid = uid
        self.group_id = self.set_group_id()
        self.max_users = max_users
        self.group_members = self.set_group_members(self.max_users)

    def __str__(self):
        return str(self.group_members)

    def set_group_id(self):
        """ Return group's ID. """
        url = 'https://api.vk.com/method/' \
              '{method}?{parameters}&v={api}&' \
              'access_token={token}'.format(method='groups.getById',
                                            api='57.1',
                                            parameters='group_ids=' + self.uid,
                                            token=MY_TOKEN)
        try:
            req = requests.get(url)
            dic = json.loads(req.text)
            id = dic['response'][0]['id']
            return id
        except:
            return 9713780

    def set_group_members(self, max_users):
        offset = 0
        lst_users = []
        resp = vk.groups.getMembers(group_id=self.group_id, offset=offset)["response"]
        while len(lst_users) < max_users and offset <= resp["count"]:
            lst_users += resp["items"]
            offset += 1000
        return lst_users

    def get_members(self):
        return self.group_members

    def new_statistic(self):
        data_values2 = [0, 0]
        lst_compacts = []
        compact = ''
        count = 0

        for user in self.group_members:
            compact += str(user) + ','
            count += 1
            if count == 100:
                lst_compacts.append(compact[:-1])
                compact = ''
                count = 0

        for compact in lst_compacts:
            req = requests.get('https://api.vk.com/method/{method}?'
                               'user_ids={u_id}&fields=uid,bdate,sex&'
                               'access_token={token}&v={api}'.format(
                method='users.get',
                token=MY_TOKEN,
                u_id=compact,
                api='57.1'))
            dic = json.loads(req.text)
            for user in dic['response']:
                if user['sex'] == 2:
                    data_values2[0] += 1
                else:
                    data_values2[1] += 1
        print('Python: мужчин - ', data_values2[0], ', женщин - ', data_values2[1])


class Group2:
    def __init__(self, uid, max_users):
        self.uid = uid
        self.group_id = self.set_group_id()
        self.max_users = max_users
        self.group_members = self.set_group_members(self.max_users)
        self.compacts = self.get_compacts()

    def __str__(self):
        return str(self.group_members)

    def set_group_id(self):
        """ Return group's ID. """
        url = 'https://api.vk.com/method/' \
              '{method}?{parameters}&v={api}&' \
              'access_token={token}'.format(method='groups.getById',
                                            api='57.1',
                                            parameters='group_ids=' + self.uid,
                                            token=MY_TOKEN)
        try:
            req = requests.get(url)
            dic = json.loads(req.text)
            id = dic['response'][0]['id']
            return id
        except:
            return 9713780

    def set_group_members(self, max_users):
        offset = 0
        lst_users = []
        resp = vk.groups.getMembers(group_id=self.group_id, offset=offset)["response"]
        while len(lst_users) < max_users and offset <= resp["count"]:
            lst_users += resp["items"]
            offset += 1000
        return lst_users

    def get_members(self):
        return self.group_members

    def get_compacts(self):
        compact = ''
        count = 0
        lst_compacts = []

        for user in self.group_members:
            compact += str(user) + ','
            count += 1
            if count == 100:
                lst_compacts.append(compact[:-1])
                compact = ''
                count = 0
        return lst_compacts

    def new_statistic_helper(self, q):
        data_values2 = [0, 0]

        while True:
            item = q.get()
            if item is None:
                break
            req = requests.get('https://api.vk.com/method/{method}?'
                               'user_ids={u_id}&fields=uid,bdate,sex&'
                               'access_token={token}&v={api}'.format(
                method='users.get',
                token=MY_TOKEN,
                u_id=item,
                api='57.1'))
            dic = json.loads(req.text)

            for user in dic['response']:
                if user['sex'] == 2:
                    data_values2[0] += 1
                else:
                    data_values2[1] += 1
        return data_values2

    def new_statistic(self):
        q = Queue(5)
        with ThreadPoolExecutor(max_workers=2) as pool:
            results = pool.submit(self.new_statistic_helper, q)
            for compact in self.compacts:
                q.put(compact)
            q.put(None)
            q.put(None)
        print('Java: мужчин - ', results.result()[0], ', женщин - ', results.result()[1])


class Group3:
    def __init__(self, uid, max_users):
        self.uid = uid
        self.group_id = self.set_group_id()
        self.max_users = max_users
        self.group_members = self.set_group_members(self.max_users)
        self.compacts = self.get_compacts()

        self._size = 5
        self._queue = []
        self._mutex = threading.RLock()
        self._empty = threading.Condition(self._mutex)
        self._full = threading.Condition(self._mutex)

    def __str__(self):
        return str(self.group_members)

    def set_group_id(self):
        """ Return group's ID. """
        url = 'https://api.vk.com/method/' \
              '{method}?{parameters}&v={api}&' \
              'access_token={token}'.format(method='groups.getById',
                                            api='57.1',
                                            parameters='group_ids=' + self.uid,
                                            token=MY_TOKEN)
        try:
            req = requests.get(url)
            dic = json.loads(req.text)
            id = dic['response'][0]['id']
            return id
        except:
            return 9713780

    def set_group_members(self, max_users):
        offset = 0
        lst_users = []
        resp = vk.groups.getMembers(group_id=self.group_id, offset=offset)["response"]
        while len(lst_users) < max_users and offset <= resp["count"]:
            lst_users += resp["items"]
            offset += 1000
        return lst_users

    def get_members(self):
        return self.group_members

    def get_compacts(self):
        compact = ''
        count = 0
        lst_compacts = []

        for user in self.group_members:
            compact += str(user) + ','
            count += 1
            if count == 100:
                lst_compacts.append(compact[:-1])
                compact = ''
                count = 0
        return lst_compacts

    def new_statistic_helper(self, q):
        data_values2 = [0, 0]

        while True:
            if data_values2[0] + data_values2[1] == 1000:
                return data_values2
            item = self.get()

            req = requests.get('https://api.vk.com/method/{method}?'
                               'user_ids={u_id}&fields=uid,bdate,sex&'
                               'access_token={token}&v={api}'.format(
                method='users.get',
                token=MY_TOKEN,
                u_id=item,
                api='57.1'))
            dic = json.loads(req.text)
            # print(dic)

            for user in dic['response']:
                if user['sex'] == 2:
                    data_values2[0] += 1
                else:
                    data_values2[1] += 1
        return data_values2

    def put(self, val):
        with self._full:
            while len(self._queue) >= self._size:
                self._full.wait()
            self._queue.append(val)
            self._empty.notify()

    def get(self):
        with self._empty:
            while len(self._queue) == 0:
                self._empty.wait()
            ret = self._queue.pop(0)
            self._full.notify()
            return ret

    def new_statistic(self):
        with ThreadPoolExecutor(max_workers=2) as pool:
            results = pool.submit(self.new_statistic_helper, self._queue)
            for compact in self.compacts:
                self.put(compact)
        self.put(None)
        self.put(None)
        print('Javascript: мужчин - ', results.result()[0], ', женщин - ', results.result()[1])
