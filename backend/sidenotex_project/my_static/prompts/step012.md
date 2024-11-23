Do have a look at my Custom User model. Initially I had email there but I decided to replace it with a hash (Its enough to find back the user on second attempt of account creation not to create another account but instead send the token again (not to lose past entries access). This made the API call where email is provided fail. 

I want the following changes. 

1) add a Name field in CustomUser model, it should be maintainable on the dashboard view. 

2) default value is Anonymous but user should be able to change it. 

3) apply corrections across my app (both in api_views and views). 