import { Component } from '@angular/core';
import {NavBarComponent} from "../nav-bar/nav-bar.component";
import {ButtonActionComponent} from "../buttons/button-action/button-action.component";
import {RouterLink} from "@angular/router";

@Component({
  selector: 'app-accuil-left-bloc',
  standalone: true,
    imports: [
        NavBarComponent,
        ButtonActionComponent,
        RouterLink
    ],
  templateUrl: './accuil-left-bloc.component.html',
  styleUrl: './accuil-left-bloc.component.scss'
})
export class AccuilLeftBlocComponent {

}
