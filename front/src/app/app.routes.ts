import { Routes } from '@angular/router';
import {NavBarComponent} from "./shared/components/nav-bar/nav-bar.component";
import {AccueilPageComponent} from "./pages/accueil-page/accueil-page.component";
import {SinglePackComponent} from "./shared/components/pack/single-pack/single-pack.component";
import {RegisterComponent} from "./pages/form/register/register.component";
import {ConnexionComponent} from "./pages/form/connexion/connexion.component";
import {SubscriptionPageComponent} from "./pages/subscription-page/subscription-page.component";
import {CancelComponent} from "./pages/subscription-page/cancel/cancel.component";
import {SuccessComponent} from "./pages/subscription-page/success/success.component";
import {GenreComponent} from "./pages/genre/genre.component";
import {MusicCardComponent} from "./shared/components/music-card/music-card.component";
import {UploadSongComponent} from "./pages/admin/upload-song/upload-song.component";
import {CategoryDetailsComponent} from "./pages/music/category-details/category-details.component";
import {UserProfilComponent} from "./pages/profile/user-profil/user-profil.component";
import {FilterSoundsComponent} from "./shared/components/filter/filter-sounds/filter-sounds.component";
import {PackDetailComponent} from "./pages/pack-detail/pack-detail.component";
import {AccountComponent} from "./pages/profile/account/account.component";
import {BillingComponent} from "./pages/profile/billing/billing.component";
import {PlansComponent} from "./pages/profile/plans/plans.component";


export const routes: Routes = [
    {
        path:'',
        component:AccueilPageComponent
    },
    {
        path: 'button',
        component: NavBarComponent
    },
    {
        path: 'single-pack',
        component: SinglePackComponent
    },
    //FORM LOG
    {
        path: 'register',
        component: RegisterComponent
    },
    {
        path: 'connexion',
        component: ConnexionComponent
    },
    {
        path: 'subscription',
        component: SubscriptionPageComponent
    },
    {
        path: 'cancel_sub',
        component: CancelComponent
    },
    {
        path: 'success',
        component: SuccessComponent
    },
    {
        path: 'category',
        component: GenreComponent
    },
    {
        path: 'music',
        component: MusicCardComponent
    },
    {
        path: 'admin',
        component: UploadSongComponent
    },
    //MUSIC
    {
        path: 'category/:id',
        component: CategoryDetailsComponent
    },
    {
        path: 'profile',
        component: UserProfilComponent,
        children: [
            { path: 'account', component: AccountComponent },
            { path: 'billing', component: BillingComponent },
            { path: 'plans', component: PlansComponent },
            { path: '', redirectTo: 'account', pathMatch: 'full' },
        ],
    },
    {
        path: 'filter',
        component: FilterSoundsComponent
    },
    {
        path: 'pack-detail/:id',
        component: PackDetailComponent
    }
];
