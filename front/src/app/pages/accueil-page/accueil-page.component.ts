import { Component } from '@angular/core';
import {NavBarComponent} from "../../shared/components/nav-bar/nav-bar.component";
import {AccuilLeftBlocComponent} from "../../shared/components/accuil-left-bloc/accuil-left-bloc.component";
import {MostRecentPackComponent} from "../../shared/components/pack/most-recent/most-recent-pack.component";
import {PopularPacksComponent} from "../../shared/components/pack/popular-pack/popular-pack.component";

@Component({
  selector: 'app-accueil-page',
  standalone: true,
    imports: [
        NavBarComponent,
        AccuilLeftBlocComponent,
        MostRecentPackComponent,
        PopularPacksComponent
    ],
  templateUrl: './accueil-page.component.html',
  styleUrl: './accueil-page.component.scss'
})
export class AccueilPageComponent {

}
