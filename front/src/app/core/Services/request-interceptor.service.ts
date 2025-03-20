import { Injectable } from '@angular/core';
import {
    HttpInterceptor,
    HttpRequest,
    HttpHandler,
    HttpEvent,
    HttpErrorResponse
} from '@angular/common/http';
import { Observable, throwError, BehaviorSubject } from 'rxjs';
import { catchError, switchMap, filter, take, tap } from 'rxjs/operators';
import { ApiManagementService } from './api-management.service';

@Injectable()
export class RequestInterceptor implements HttpInterceptor {
    private isRefreshing = false;
    private refreshTokenSubject: BehaviorSubject<any> = new BehaviorSubject<any>(null);

    constructor(private apiManagementService: ApiManagementService) {}

    intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
        console.log('Interceptor is processing the request:', req.url);
        return next.handle(req).pipe(
            catchError(error => {
                console.log('Error intercepted:', error);
                if (error instanceof HttpErrorResponse && error.status === 401) {
                    console.log('Handling 401 error');
                    return this.handle401Error(req, next);
                } else {
                    return throwError(error);
                }
            })
        );
    }

    private handle401Error(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
        console.log('handle401Error called');
        if (!this.isRefreshing) {
            this.isRefreshing = true;
            this.refreshTokenSubject.next(null);

            return this.refreshToken().pipe(
                switchMap((token: any) => {
                    this.isRefreshing = false;
                    this.refreshTokenSubject.next(token);
                    console.log('Retrying original request');
                    return next.handle(req);
                }),
                catchError((err) => {
                    this.isRefreshing = false;
                    console.log('Failed to refresh token:', err);
                    // Optionnel : Rediriger vers la page de connexion ou autre action
                    return throwError(err);
                })
            );
        } else {
            return this.refreshTokenSubject.pipe(
                filter(token => token != null),
                take(1),
                switchMap(() => {
                    console.log('Retrying original request after refresh');
                    return next.handle(req);
                })
            );
        }
    }

    private refreshToken(): Observable<any> {
        console.log('Attempting to refresh token');
        return this.apiManagementService.post('api/token/refresh/').pipe(
            tap(() => console.log('Token refreshed successfully')),
            catchError(error => {
                console.log('Error refreshing token:', error);
                return throwError(error);
            })
        );
    }
}
