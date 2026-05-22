from microbit import *
import music
import speech
import struct

## 初期設定
# 右のモーターを止める
pin13.write_analog(511)
# 左のモーターを止める
pin14.write_analog(511)
# 右のモーターに送る信号の周期を1秒に設定する
pin13.set_analog_period(1000)
# 左のモーターに送る信号の周期を1秒に設定する
pin14.set_analog_period(1000)
# 右のモーターのブレーキを解除する
pin15.write_digital(0)
# 左のモーターのブレーキを解除する
pin16.write_digital(0)
# 左旋回フラグ
left_turn = 0
# 右旋回フラグ
right_turn = 0

# 超音波センサーのアドレス
address = 0
# 超音波センサーの起動時間
start_time = 0
# 反射時間
reflection_time = 0
# 反射時間(上位桁)
reflection_time_h = 0
# 反射時間(下位桁)
reflection_time_l = 0
# 超音波センサーのレスポンス
response = 0
# 反射距離
reflaction_distance = 0
# 障害物との距離
distance = 0


# 障害物との距離を確認する
def get_distance_from_obstacles():
    global address, distance
    address = 0x2C
    distance = 0
    # 超音波センサーと通信して反射距離を取得する
    conn_i2c()
    # 反射距離が100cm以内の場合
    if 0 <= reflaction_distance and reflaction_distance <= 1000:
        # 反射距離を四捨五入して障害物との距離にセットする
        distance = round(reflaction_distance)
    else:
        # 障害物との距離をリセットする
        distance = 0


# I2Cで超音波センサーと通信する
def conn_i2c():
    global start_time, reflection_time, reflection_time_h, reflection_time_l, response, reflaction_distance
    start_time = running_time()
    reflection_time = 0
    reflection_time_h = 0
    reflection_time_l = 0
    response = 0
    reflaction_distance = 0
    # 起動して50ms未満または正常な結果が返って来ない場合は繰り返す
    while reflection_time_h == 0 and reflection_time_l and running_time() - start_time < 50:
        # 超音波センサー(アドレス：44)に値：51を送り、使用を開始する
        command_51 = struct.pack(">B", 51)
        i2c.write(address, bytearray(command_51), False)
        # 0.1秒待機する
        sleep(100)
        # レスポンスを取得する
        response = int.from_bytes(i2c.read(address, 1, False), "big")
        # センサーの使用が正常に開始された場合
        if response == 1:
            # アドレス：44に値：16を送り、反射時間の上位桁と下位桁の和の取得を実行する
            command_16 = struct.pack(">B", 16)
            i2c.write(address, bytearray(command_16), False)
            # 0.1秒待機する
            sleep(100)
            # 反射時間の上位桁と下位桁の和を取得する
            reflection_time = int.from_bytes(i2c.read(address, 1, False), "big")
            # アドレス：44に値：15を送り、反射時間(上位桁)の取得を実行する
            command_15 = struct.pack(">B", 15)
            i2c.write(address, bytearray(command_15), False)
            # 0.1秒待機する
            sleep(100)
            # 反射時間(上位桁)を取得する
            reflection_time_h = int.from_bytes(i2c.read(address, 1, False), "big")
            # アドレス：44に値：14を送り、反射時間(下位桁)の取得を実行する
            command_14 = struct.pack(">B", 14)
            i2c.write(address, bytearray(command_14), False)
            # 0.1秒待機する
            sleep(100)
            # 反射時間(下位桁)を取得する
            reflection_time_l = int.from_bytes(i2c.read(address, 1, False), "big")
            # 反射時間の上位桁と下位桁の和が誤っている場合
            if reflection_time != reflection_time_h + reflection_time_l:
                # 反射時間をリセットする
                reflection_time_h = 0
                reflection_time_l = 0
            else:
                # 次の方法で反射時間から反射距離を取得する
                # 1. 上位桁に256をかけて10進数に変換して下位桁と加算し、超音波センサーのノイズ補正値：160を引く
                # 2. 1を2で割り、片道の時間を算出する
                # 3. 超音波の速度：0.315（mm/μs）をかけて反射距離を算出する
                reflaction_distance = (
                    (reflection_time_h * 256 + reflection_time_l - 160) / 2 * 0.315
                )


### メインプログラム
while True:
    # 右のモーターを止める
    pin13.write_analog(511)
    # 左のモーターを止める
    pin14.write_analog(511)
    # 1秒待機する
    sleep(1000)
    if left_turn == 0 and right_turn == 0:
        # 内蔵されている音楽を鳴らす
        # music.play(music.ENTERTAINER, pin=pin8, wait=True, loop=False)
        # 1秒待機する
        sleep(1000)
    # 内蔵されている音楽を鳴らす
    # music.play(music.BA_DING, pin=pin8, wait=True, loop=False)
    # 1秒待機する
    sleep(1000)
    # 障害物との距離を確認する
    get_distance_from_obstacles()
    # 1秒待機する
    sleep(1000)
    # 障害物との距離が10cmの場合
    if 0 < distance and distance < 100:
        # 音声を出力する
        speech.say("Detect obstacles", speed=120, pitch=50, throat=50, mouth=200)
        # 1秒待機する
        sleep(1000)
        # 内蔵されている音楽を鳴らす
        music.play(music.DADADADUM, pin=pin8, wait=True, loop=False)
        # 1秒待機する
        sleep(1000)
        # 怒りマークを表示する
        display.show(Image.ANGRY)
        # 1秒待機する
        sleep(1000)
        # LEDの表示を消す
        display.clear()
    # 3回左回旋する
    elif left_turn < 3:
        # 右のモーターを回す
        pin13.write_analog(1023)
        # 左のモーターを回す
        pin14.write_analog(910)
        # 2秒待機する
        sleep(2000)
        # 音声を出力する
        speech.say("Turn Left", speed=120, pitch=50, throat=50, mouth=200)
        # 1秒待機する
        sleep(1000)
        # 左矢印を表示する
        display.show(Image.ARROW_E)
        # 1秒待機する
        sleep(1000)
        # LEDの表示を消す
        display.clear()
        # 右のモーターを回す
        pin13.write_analog(1023)
        # 左のモーターを回す
        pin14.write_analog(0)
        # 1.2秒待機する
        sleep(1150)
        # 左旋回フラグをカウントアップする
        left_turn += 1
    # 対角線上に走行し右回旋する
    elif left_turn == 3:
        # 右のモーターを回す
        pin13.write_analog(1023)
        # 左のモーターを回す
        pin14.write_analog(910)
        # 8秒待機する
        sleep(8000)
        # 音声を出力する
        speech.say("Turn Right", speed=120, pitch=50, throat=50, mouth=200)
        # 1秒待機する
        sleep(1000)
        # 右矢印を表示する
        display.show(Image.ARROW_W)
        # 1秒待機する
        sleep(1000)
        # LEDの表示を消す
        display.clear()
        # 右のモーターを回す
        pin13.write_analog(0)
        # 左のモーターを回す
        pin14.write_analog(1023)
        # 1.2秒待機する
        sleep(1200)
        # 左旋回フラグをカウントアップする
        left_turn += 1
    # 2回右回旋する
    elif right_turn < 2:
        # 右のモーターを回す
        pin13.write_analog(1023)
        # 左のモーターを回す
        pin14.write_analog(910)
        # 2秒待機する
        sleep(2000)
        # 音声を出力する
        speech.say("Turn Right", speed=120, pitch=50, throat=50, mouth=200)
        # 1秒待機する
        sleep(1000)
        # 右矢印を表示する
        display.show(Image.ARROW_W)
        # 1秒待機する
        sleep(1000)
        # LEDの表示を消す
        display.clear()
        # 右のモーターを回す
        pin13.write_analog(0)
        # 左のモーターを回す
        pin14.write_analog(1023)
        # 1.2秒待機する
        sleep(1200)
        # 右旋回フラグをカウントアップする
        right_turn += 1
    # 出発地点まで走行する
    else:
        # 右のモーターを回す
        pin13.write_analog(1023)
        # 左のモーターを回す
        pin14.write_analog(910)
        # 4秒待機する
        sleep(4000)
        # フラグをリセットする
        left_turn = 0
        right_turn = 0
