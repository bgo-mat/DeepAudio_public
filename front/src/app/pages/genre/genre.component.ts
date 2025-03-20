import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { Category } from '../../shared/models/category.model';
import { CategoryService } from "../../core/Services/music/category/category.service";
import {NavBarComponent} from "../../shared/components/nav-bar/nav-bar.component";
import {NgForOf, NgIf} from "@angular/common";
import {PackCardComponent} from "../../shared/components/pack/pack-card/pack-card.component";
import {PopularPacksComponent} from "../../shared/components/pack/popular-pack/popular-pack.component";

@Component({
    selector: 'genre-component',
    templateUrl: 'genre.component.html',
    standalone: true,
    imports: [
        NavBarComponent,
        NgForOf,
        NgIf,
        PackCardComponent,
        PopularPacksComponent
    ],
    styleUrls: ['./genre.component.scss']
})
export class GenreComponent implements OnInit {
    public groupedCategories: { title: string; genres: Category[] }[] = [];

    constructor(private categoryService: CategoryService,  private router: Router) {}

    ngOnInit(): void {
        this.categoryService.getAllCategory().subscribe(
            (data: Category[]) => {
                this.groupCategories(data);
            },
            error => {
                console.error('Error fetching categories:', error);
            }
        );
    }

    private groupCategories(categories: Category[]): void {
        const genreGroups = {
            'Hip Hop / R&B': ['Hip Hop', 'Trap', 'R&B', 'Soul', 'Reggaeton', 'Dancehall', 'Moombahton', 'Future Bass', 'Glitch Hop'],
            'House / Techno': ['Techno', 'House', 'Tech House', 'Deep House', 'Disco', 'Electro', 'Minimal Techno', 'Hard Techno', 'UK Garage', 'Progressive House', 'Hardstyle'],
            'Pop / EDM': ['Pop', 'EDM', 'Trance', 'Psytrance', 'Future House', 'Fidget House', 'Tropical House'],
            'Bass Music': ['Drum and Bass', 'Jungle', 'Drumstep', 'Breakbeat', 'Dubstep', 'Tearout Dubstep', 'Grime', 'Leftfield Bass'],
            'Live Sounds': ['Rock', 'Indie Dance', 'Jazz', 'Blues', 'Heavy Metal', 'Funk', 'Dub', 'Reggae', 'Folk', 'Country'],
            'Electronic': ['Downtempo', 'Ambient', 'Synthwave', 'IDM', 'Experimental', 'Chiptune', 'Trip Hop', 'Footwork'],
            'Global': ['African', 'Asian', 'Brazilian', 'Caribbean', 'Indian', 'Latin American', 'Middle Eastern', 'South Asian'],
            'Cinematic / FX': ['Cinematic', 'Game Audio']
        };

        this.groupedCategories = Object.entries(genreGroups).map(([title, genreNames]) => ({
            title,
            genres: categories.filter(category => genreNames.includes(category.name))
        }));
    }

    public onGenreClick(categoryId: number): void {
        console.log("Clicked category ID:", categoryId);
        this.router.navigate(['/category', categoryId]);
    }
}
