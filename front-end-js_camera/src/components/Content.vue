<template>
  <div class="publish">
    <!-- <video ref="video"></video>
    <canvas style="display: none" id="canvasCamera"></canvas> -->
    <!-- <div v-if="imgSrc" class="img_bg_camera">
      <img :src="imgSrc" class="tx_img" />
    </div> -->
    <el-row style="text-align: center;">
    <!-- <button @click="OpenCamera">打开摄像头</button> -->
    <el-button type="primary" @click="OpenCamera" > 开始 </el-button>
    <el-button type="primary" @click="CloseCamera" > 停止 </el-button>
    <!-- <el-button type="primary" @click="setImage" > 识别 </el-button> -->
    </el-row>
    <el-row style="text-align: center;">
    <el-image
                :src="video_url"
                style="width: 800px; height: 350px; margin-bottom:-4px"
              >
      </el-image>
  </el-row>

  <div style="width:100%;height:100px;border:1px solid red;">
      <canvas id="canvas"></canvas>
      <span style="padding: 0 10%;"></span>
      <canvas id="playChart"></canvas>
    </div>

  <el-table
        :data="table_data"
        height="390"
        style="width: 600px; text-align: center; margin: 10px auto;"
        :key="tableKey"
        element-loading-text="数据正在处理中，请耐心等待"
        element-loading-spinner="el-icon-loading"
        lazy
      >
        <el-table-column label="音频识别结果" align="center" width="200px" prop="class">
        </el-table-column>
        <el-table-column label="余弦距离" align="center" width="200px" prop="prob">
        </el-table-column>
        <!-- <el-table-column label="结果图片" align="center" width="720px" prop="imageUrl">
          <template slot-scope="scope">
            <el-image
              style="width: 700px; height: 300px; margin-bottom:-4px"
              :src="scope.row.imageUrl"
            >
            </el-image>
          </template>
        </el-table-column> -->
        <el-table-column label="更新时间" align="center" width="200px" prop="time">
        </el-table-column>
      </el-table>
  </div>
</template>

<script>
import axios from "axios";
import Recorder from 'js-audio-recorder'
  const lamejs = require('lamejs')
  const recorder = new Recorder({
    sampleBits: 16,                 // 采样位数，支持 8 或 16，默认是16
    sampleRate: 44100,              // 采样率，支持 11025、16000、22050、24000、44100、48000，根据浏览器默认值，我的chrome是48000
    numChannels: 1,                 // 声道，支持 1 或 2， 默认是1
    // compiling: false,(0.x版本中生效,1.x增加中)  // 是否边录边转换，默认是false
  })

export default {
  data() {
    return {
      mediaStreamTrack: {},
      video_stream: '', // 视频stream
      image: '', // 拍照图片
      canvas: null,
      context: null,
      params: null,
      server_url: "http://127.0.0.1:5004/",
      video_url: "http://127.0.0.1:5004/video_feed0",
      // server_url: "http://10.193.224.113:80/",
      table_data: null,
      //波浪图-录音
      drawRecordId:null,
      oCanvas : null,
      ctx : null,
      srcList: null,
      start: false,
      //波浪图-播放
      drawPlayId:null,
      pCanvas : null,
      pCtx : null,
      tableKey: null,
    };
  },
  created: function () {
    document.title = "音视频识别系统";

    setInterval(() => {
      if (this.start === true){
        this.video_url = "http://127.0.0.1:5004/video_feed0"
        this.startCanvas()
      }
      else{
        this.video_url = ""
        this.closeCanva()
      }
    },
      10);
    setInterval(() => {
      if (this.start === true){
       this.voiceRec()
      }
    },
    3000)
  },
  mounted() {
    // 进入页面 自动调用摄像头
    // this.getCamera();
    // this.getPermission();
    // this.startRecorder()
  },
  methods: {
    // 调用打开摄像头功能
    getCamera() {
      // 获取 canvas 画布
      this.canvas = document.getElementById('canvasCamera');
      this.canvas.width = 1280
      this.canvas.height = 720
      this.context = this.canvas.getContext('2d');
      // 旧版本浏览器可能根本不支持mediaDevices，我们首先设置一个空对象
      if (navigator.mediaDevices === undefined) {
        navigator.mediaDevices = {};
      }
      // 正常支持版本
      navigator.mediaDevices
        .getUserMedia({
          video: { width: 1280, height: 720 },
          audio: true,
        })
          .then((stream) => {
          // 摄像头开启成功
          this.mediaStreamTrack = typeof stream.stop === 'function' ? stream : stream.getTracks()[0];
          this.video_stream = stream;
          this.$refs.video.srcObject = stream;
          this.$refs.video.play();
        })
    },
    bigImg(url) {
      this.srcList[0] = url;
    },
    // 识别
    voiceRec() {
      // console.log('拍照');
      // 取得图片
      // this.context.drawImage(
      //   this.$refs.video,
      //   0,
      //   0,
      //   1280,
      //   720,
      // );
      // 获取图片base64链接
      let toltime = recorder.duration;//录音总时长
      let fileSize = recorder.fileSize;//录音总大小
      let wavBlob = recorder.getWAVBlob()
      this.startRecorder()
      // let audioBlob = new File([wavBlob], '文件名.wav', { type: 'audio/wav' })
      // var file = this.blobToFile(wavBlob, "my-recording.wav")
      // const image = this.canvas.toDataURL('image/png', 1);

      // this.params = {
      //   "image": image
      // }
      // axios.post(this.server_url + "face_recognition", this.params).then(
      //   res => {
      //     this.table_data = [{
      //      class: res.data["class"],
      //      prob: res.data["prob"],
      //      time: res.data["time"],
      //     //  imageUrl: "data:image/jpg;base64," + res.data["image"],
      //     imageUrl: this.server_url + "video_feed0"
      //    }
      //   ]
      //   console.log(this.table_data);
      //     this.tableKey = Math.random()
      //     // alert("识别完成")
      //   }
      // )
      let data = new FormData();
      data.append('file', wavBlob);
      
      axios.post(this.server_url + "audio_recognition", data, {headers:{
        'Content-Type': 'multipart/form-data',
      }}).then(res => {
        const tableLength = Object.keys(res.data).length
        this.table_data = []
        console.log(res.data)
        for (let i = 0; i < tableLength; i++) {
        let  rec_data = res.data[i]
        this.table_data.push({
           class: rec_data["class"],
           prob: rec_data["prob"],
           time: rec_data["time"],
        })
    }
      this.tableKey = Math.random()
    })
    },
    // 打开摄像头
    OpenCamera() {
      // console.log('打开摄像头');
      // this.getCamera();
      this.startRecorder()
      this.start = true
    },
    // 关闭摄像头
    CloseCamera() {
      this.start = false
      // console.log('关闭摄像头');
      // this.$refs.video.srcObject.getTracks()[0].stop();
      recorder.stop()
    },
    startCanvas(){
        //录音波浪
        this.oCanvas = document.getElementById('canvas');
        this.oCanvas.width = 200
        this.oCanvas.height = 50
        this.ctx = this.oCanvas.getContext("2d");
        //播放波浪
        // this.pCanvas = document.getElementById('playChart');
        // this.pCtx = this.pCanvas.getContext("2d");
      },
      closeCanva(){
        this.ctx = null
      },
      startRecorder () {
        recorder.start().then(() => {
          this.drawRecord();//开始绘制图片
        }, (error) => {
          // 出错了
          console.log(`${error.name} : ${error.message}`);
        });
      },
      stopRecorder () {
        recorder.stop()
        this.drawRecordId && cancelAnimationFrame(this.drawRecordId);
        this.drawRecordId = null;
      },
      getRecorder(){
        let toltime = recorder.duration;//录音总时长
        let fileSize = recorder.fileSize;//录音总大小
 
        //录音结束，获取取录音数据
        let PCMBlob = recorder.getPCMBlob();//获取 PCM 数据
        let wav = recorder.getWAVBlob();//获取 WAV 数据
 
        let channel = recorder.getChannelData();//获取左声道和右声道音频数据
 
      },
      getPermission(){
        Recorder.getPermission().then(() => {
          this.$Message.success('获取权限成功')
        }, (error) => {
          console.log(`${error.name} : ${error.message}`);
        });
      },
      getMp3Data(){
        const mp3Blob = this.convertToMp3(recorder.getWAV());
        recorder.download(mp3Blob, 'recorder', 'mp3');
      },
      convertToMp3(wavDataView) {
        // 获取wav头信息
        const wav = lamejs.WavHeader.readHeader(wavDataView); // 此处其实可以不用去读wav头信息，毕竟有对应的config配置
        const { channels, sampleRate } = wav;
        const mp3enc = new lamejs.Mp3Encoder(channels, sampleRate, 128);
        // 获取左右通道数据
        const result = recorder.getChannelData()
        const buffer = [];
 
        const leftData = result.left && new Int16Array(result.left.buffer, 0, result.left.byteLength / 2);
        const rightData = result.right && new Int16Array(result.right.buffer, 0, result.right.byteLength / 2);
        const remaining = leftData.length + (rightData ? rightData.length : 0);
 
        const maxSamples = 1152;
        for (let i = 0; i < remaining; i += maxSamples) {
          const left = leftData.subarray(i, i + maxSamples);
          let right = null;
          let mp3buf = null;
 
          if (channels === 2) {
            right = rightData.subarray(i, i + maxSamples);
            mp3buf = mp3enc.encodeBuffer(left, right);
          } else {
            mp3buf = mp3enc.encodeBuffer(left);
          }
 
          if (mp3buf.length > 0) {
            buffer.push(mp3buf);
          }
        }
 
        const enc = mp3enc.flush();
 
        if (enc.length > 0) {
          buffer.push(enc);
        }
 
        return new Blob(buffer, { type: 'audio/mp3' });
      },
      blobToFile(theBlob , fileName){
          var b = theBlob;
          //Add properties to the blob
          b.lastModifiedDate = new Date();
          b.name = fileName;
          return theBlob;
        },
      /**
       * 绘制波浪图-录音
       * */
       drawRecord () {

        // 用requestAnimationFrame稳定60fps绘制
        this.drawRecordId = requestAnimationFrame(this.drawRecord);
 
        // 实时获取音频大小数据
        let dataArray = recorder.getRecordAnalyseData(),
            bufferLength = dataArray.length;
 
        // 填充背景色
        this.ctx.fillStyle = 'rgb(200, 200, 200)';
        this.ctx.fillRect(0, 0, this.oCanvas.width, this.oCanvas.height);
 
        // 设定波形绘制颜色
        this.ctx.lineWidth = 2;
        this.ctx.strokeStyle = 'rgb(0, 0, 0)';
 
        this.ctx.beginPath();
        var sliceWidth = this.oCanvas.width * 1.0 / bufferLength, // 一个点占多少位置，共有bufferLength个点要绘制
                x = 0;          // 绘制点的x轴位置
 
        for (var i = 0; i < bufferLength; i++) {
          var v = dataArray[i] / 128.0;
          var y = v * this.oCanvas.height / 2;
 
          if (i === 0) {
            // 第一个点
            this.ctx.moveTo(x, y);
          } else {
            // 剩余的点
            this.ctx.lineTo(x, y);
          }
          // 依次平移，绘制所有点
          x += sliceWidth;
        }
 
        this.ctx.lineTo(this.oCanvas.width, this.oCanvas.height / 2);
        this.ctx.stroke();
      },
  },
};
</script>

<style scoped>
video {
  width: 100%;
  height: 300px;
}
canvas {
  width: 100%;
  height: 100px;
}
button {
  width: 100px;
  height: 40px;
  position: relative;
  bottom: 0;
  left: 0;
  background-color: rgb(22, 204, 195);
}

</style>
