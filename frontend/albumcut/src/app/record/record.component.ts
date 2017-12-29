import { Component, OnInit, Input } from '@angular/core';
import { Album } from '../shared/models';

@Component({
  selector: 'app-record',
  templateUrl: './record.component.html',
  styleUrls: ['./record.component.css']
})
export class RecordComponent implements OnInit {


	@Input() albums: Album[];

  constructor() { }

  ngOnInit() {
  }

  

}
