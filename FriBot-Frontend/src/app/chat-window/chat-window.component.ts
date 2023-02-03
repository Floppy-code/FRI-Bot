import { formatDate } from '@angular/common';
import { Component} from '@angular/core';
import { faPaperPlane, faWindowMinimize, faEnvelope} from '@fortawesome/free-regular-svg-icons';
import { RestApiService } from '../shared/rest-api.service';
import { FormGroup, FormControl } from '@angular/forms';

@Component({
  selector: 'chat-window',
  templateUrl: './chat-window.component.html',
  styleUrls: ['./chat-window.component.scss']
})


export class ChatWindowComponent {
  constructor(public restApi: RestApiService) {}

  faArrowRight = faPaperPlane;
  faMinimize = faWindowMinimize;
  faEmail = faEnvelope;
  reactiveForm = new FormGroup({
    message: new FormControl(''),
  });


  displayChat: boolean = true
  writing: boolean = false
  startTime = formatDate(Date.now(),'HH:mm', 'en-US'); 
  //startTime: string = new Date().toTimeString()
  messages: Array<Message> = []//[new Message("FRI", "Ahoj, ako ti môžem pomôcť?", "10:55"), new Message("student", "Kedy bude chatbot hotový?", "10:55"), new Message("FRI", "Dobrá otázka.", "10:58"), new Message("FRI", "Robíme všetko pre to, aby to bolo čo najskôr?", "10:58")]

  onMouseEnter() {
    console.log("jou")
  }

  addStudentMessage(text : string) {
    if (text !== '') {
      this.messages.push(new Message("student", text, new Date().toTimeString()))
      this.reactiveForm.reset()
      this.writing = true
      this.restApi.getAnswer(text).subscribe(data => {
        console.log(data)
        this.messages.push(new Message("fri", data.prediction + "", new Date().toTimeString()))
        this.writing = false
      })
    }
  }
}

export class Message {
  author: string
  text: string
  time: string

  constructor(author:string, text:string, time:string) {
      this.author = author;
      this.text = text;
      this.time = time;
  }
}