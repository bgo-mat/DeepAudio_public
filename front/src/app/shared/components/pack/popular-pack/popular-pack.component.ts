import { Component, Input, OnInit } from '@angular/core';
import { PackCardComponent } from "../pack-card/pack-card.component";
import { PackService } from "../../../../core/Services/music/pack/pack.service";
import { Pack } from "../../../models/pack.model";
import { NgForOf } from "@angular/common";

@Component({
  selector: 'app-popular-packs',
  templateUrl: 'popular-pack.component.html',
  standalone: true,
  imports: [
    PackCardComponent,
    NgForOf
  ],
  styleUrls: ['popular-pack.component.scss']
})
export class PopularPacksComponent implements OnInit {
  @Input() name: string = 'most popular';
  public packs: Pack[] = [];
  public title: string = '';

  constructor(private packService: PackService) {}

  ngOnInit(): void {

    let ordering = 'number_of_downloads';
    this.title = 'Popular in your area';

    if (this.name.toLowerCase() === 'most recent') {
      ordering = '-created_at';
      this.title = 'Most Recent';
    }

    this.packService.getPacks(ordering).subscribe(
        (data: any) => {
          console.log("caca", data)
          this.packs = data.results.map((item: any) => ({
            id: item.id,
            title: item.name,
            genre: item.genre_names[0],
            imageUrl: item.image || 'assets/test.png'
          }));
        },
        error => {
          console.error('Erreur lors du chargement des packs:', error);
        }
    );
  }


  public getPackWithId(id: number) {
    this.packService.getPackById(id).subscribe(
        (data: any) => {
          console.log(data)
        }
    )
  }
}
