import { Component , TemplateRef, OnInit} from '@angular/core';
import { BsModalRef, BsModalService } from 'ngx-bootstrap/modal';

import { DataService } from './shared/dataService';
import { Album } from './shared/models';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})

export class AppComponent implements OnInit {
  title = 'app';

  public modalRef: BsModalRef;
  public albums: Album[];
  public message: string;

  constructor(private modalService: BsModalService, private dataService: DataService) {}

  public openModal(template: TemplateRef<any>) {
    this.modalRef = this.modalService.show(template);
  }

  ngOnInit() {
    
        this.dataService
            .getAll<Album[]>('albums')
            .subscribe((data: Album[]) => {
            	this.albums = new Array<Album>();
            	for(var album of data){
            		this.albums.push(new Album(album));
            	}

            },
            error => () => {
                this.message = 'Error!';
            },
            () => {
                this.message = 'OK';
            });

        

    }
}
