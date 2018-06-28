# Summary
 The website and app for ListingsThatFit. ListingsThatFit is a website that emails you ebay clothing listings that fit your sizing information, weekly, from specific sellers. Built as a final project for Harvard's CS50 MOOC. 

Roadmap
------
1. Make database tables
  * Users
    * Shirt size specifics + brands/price guidelines
    * Shoe size specics + brands/price guidelines
    * Jacket size specifics + brands/price guidelines
    * Suit size specifics + brands/price guidelines
    * Pants size specifics + brands/price guidelines
    * Custom keyword watch list
    * Subscribed sellers
  * Sellers
2. Write functions to query ebay with user preferences
3. Write site
  * Registration
  * Preferences
    * Size preferences
    * Subscribed sellers
    * Notification schedule 
4. Have a MVP for the site I've wanted to build since 2014

# Rough MVP todo (I actually update this)
* [X] BeautifulSoup patterns to match sportcoat measurement templates
* [X] measurementType model
* [X] measurements link table
* [X] fully flesh out items table
* [X] script to scour template using BS and create item entry (only sportcoats for now)
* [ ] script to pull down all items and create entries for items
  * [X] pull down and create models for Suits
  * [X] pull down and create models for sportcoats
  * [ ] pull down and create models for casual shirts
  * [ ] pull down and create models for dress shirts 
  * [ ] pull down and create models for pants
  * [ ] pull down and create models for coats and jackets
  * [ ] pull down and create models for sweaters
* [ ] Measurement + tolerance association table
* [ ] Foreign key linkup to above association table
* [ ] Query to search for matching listings for User's measurements + tolerances
* [ ] Query for listings matching ad-hoc measurements + tolerances
* [ ] query to search for all items that match ad-hoc input measurements
* [ ] plaintext report generation for query results that can be output to an email
* [ ] script to update items table once items have expired
* [ ] add user measurements (+ tolerances) to user model
* [ ] UI to add measurements (+ tolerances) to user account
* [ ] query to search for all items that match user measurements
* [ ] query to search for all items that match user sizes
* [ ] UI display for all matches (sizes and measurements)
* [ ] email functionality
* [ ] buy URL
* [ ] deploy to server
* [ ] link URL to server