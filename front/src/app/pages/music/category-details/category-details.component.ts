import { Component, OnInit } from '@angular/core';
import {ActivatedRoute, Router, RouterLink} from '@angular/router';
import { CategoryService } from '../../../core/Services/music/category/category.service';
import {PackCardComponent} from "../../../shared/components/pack/pack-card/pack-card.component";
import {MusicCardComponent} from "../../../shared/components/music-card/music-card.component";
import {NgClass, NgForOf, NgIf} from "@angular/common";
import {NavBarComponent} from "../../../shared/components/nav-bar/nav-bar.component";
import {PackService} from "../../../core/Services/music/pack/pack.service";
import {HeaderMusicComponent} from "../../../shared/components/header-music/header-music.component";
import {FilterSoundsComponent} from "../../../shared/components/filter/filter-sounds/filter-sounds.component";

@Component({
  selector: 'app-category-details',
  templateUrl: './category-details.component.html',
  standalone: true,
    imports: [
        PackCardComponent,
        MusicCardComponent,
        NgIf,
        NgForOf,
        NavBarComponent,
        NgClass,
        RouterLink,
        HeaderMusicComponent,
        FilterSoundsComponent
    ],
  styleUrls: ['./category-details.component.scss']
})
export class CategoryDetailsComponent implements OnInit {
  public category: any;
  public viewMode: string = 'sounds';

  constructor(
      private categoryService: CategoryService,
      private route: ActivatedRoute,
      private router: Router,
      private packService: PackService
  ) {}

  ngOnInit(): void {
    const categoryId = Number(this.route.snapshot.paramMap.get('id'));
    this.categoryService.getCategoryByID(categoryId).subscribe(
        (response) => {
          this.category = response;
          console.log('Reponse', this.category)
        },
        (error) => {
          console.error('Error fetching category details:', error);
        }
    );
  }

  navigateToPackDetail(pack: any): void {
    this.packService.setPack(pack);
    this.router.navigate(['/pack-detail', pack.id]);
  }
}
