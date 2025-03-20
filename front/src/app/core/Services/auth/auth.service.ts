import {Injectable} from '@angular/core';
import {ApiManagementService} from "../api-management.service";
import {BehaviorSubject, Observable, of} from 'rxjs';
import {catchError, map, tap} from 'rxjs/operators';

@Injectable({
    providedIn: 'root'
})
export class AuthService {

    private userStatus$ = new BehaviorSubject<{ isConnected: boolean; role: string | null; tokens: number }>({ isConnected: false, role: null, tokens: 0 });

    constructor(private apiManagementService: ApiManagementService) { }

    public isConnect(): Observable<{ isConnected: boolean; role: string | null; tokens: number }> {
        return this.apiManagementService.get('api/user').pipe(
            map((response: any) => {
                return response && response.length > 0
                    ? {isConnected: true, role: response[0].roles || null, tokens: response[0].tokens || 0}
                    : {isConnected: false, role: null, tokens: 0};
            }),
            tap(userStatus => this.userStatus$.next(userStatus)), // Met à jour le BehaviorSubject
            catchError(() => {
                const fallbackStatus = { isConnected: false, role: null, tokens: 0 };
                this.userStatus$.next(fallbackStatus);
                return of(fallbackStatus);
            })
        );
    }

    public getUserStatus(): Observable<{ isConnected: boolean; role: string | null; tokens: number }> {
        return this.userStatus$.asObservable();
    }

    public logOut(): Observable<any> {
        return this.apiManagementService.post('api/auth/logout/', {}).pipe(
            tap(() => {
                this.userStatus$.next({ isConnected: false, role: null, tokens: 0 });
            }),
            catchError(error => {
                console.error('Erreur lors de la déconnexion:', error);
                return of(null);
            })
        );
    }

    public signIn(email: string, password: string, accept_newsletter:boolean) {
        return this.apiManagementService.post('api/auth/signup/', { email, password, accept_newsletter });
    }

    public logIn(email: string, password: string, remember_me: boolean = false): Observable<any> {
        return this.apiManagementService.post('api/auth/login/', { email, password, remember_me }).pipe(
            tap(() => {
                this.isConnect().subscribe();
            })
        );
    }



    public initializeUserStatus(): void {
        this.isConnect().subscribe();
    }
}
