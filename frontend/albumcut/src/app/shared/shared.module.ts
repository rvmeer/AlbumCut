import { CommonModule } from '@angular/common';
import { HTTP_INTERCEPTORS } from '@angular/common/http';
import { NgModule } from '@angular/core';
import { RouterModule } from '@angular/router';


import { CustomInterceptor, DataService } from './dataService';

@NgModule({
    imports: [CommonModule, RouterModule],
    declarations: [],
    providers: [DataService,
        {
            provide: HTTP_INTERCEPTORS,
            useClass: CustomInterceptor,
            multi: true,
        }],
})

export class SharedModule { }