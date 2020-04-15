import os
from mindreader.saver import Saver


def test_saver_parser_result_pose(database, data_dir):
    with open(data_dir / "pose_parser_result.json", 'r') as f:
        pose_parser_result = f.read()

    url = database.url  # extract url from our database
    saver = Saver(url)
    saver.save('pose', pose_parser_result)

    snapshot = database.get_snapshot_by_id(43, "3cb5037b-64eb-44e6-a747-bbac4616135e-test")  # metadata of pose
    pose = snapshot['topics']['pose']

    assert pose['translation']['x'] == 0.4873843491077423
    assert pose['translation']['y'] == 0.007090016733855009
    assert pose['translation']['z'] == -1.1306129693984985

    assert pose['rotation']['x'] == 0.9571326384559261
    assert pose['rotation']['y'] == -0.26755994585035286
    assert pose['rotation']['z'] == -0.021271118915446748
    assert pose['rotation']['w'] == 0.9571326384559261


# def test_save_user_from_cli(database, data_dir):
#     user_path = data_dir/'snapshot.json'
#     command = f"python -m mindreader.saver save user ./tests/data/user.json"
#     os.system(command)
#
#     user = database.get_user_by_id(781)
#
#     assert user['user_id'] == 781
#     assert user['username'] == "Yosi"
#     assert user['birthday'] == 424244422
#     assert user['gender'] == "female"
