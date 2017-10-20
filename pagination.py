from sqlalchemy import and_


class Pagination:
    def __init__(self, page, per_page, total_count):
        self.page = page
        self.per_page = per_page
        self.total_count = total_count

    def validate(self):
        """Validate own fields"""
        if self.page <= 0 or self.page > self.last:
            raise ValueError('Requested page not found')
        if self.per_page <= 0:
            raise ValueError('per_page parameter must be greater than 0')

    @property
    def next(self):
        """Get next page number"""
        if self.page == self.last:
            # Last page has to next page
            return None

        return self.page + 1

    @property
    def prev(self):
        """Get previous page number"""
        if self.page == 1:
            # First page has no prev page
            return None

        return self.page - 1

    @property
    def last(self):
        """Get last page number"""
        if self.total_count == 0:
            # First page will be the last in this case
            return 1

        return (self.total_count // self.per_page +
                (self.total_count % self.per_page > 0))

    @property
    def start_id(self):
        """Return lower id boundary"""
        return (self.page - 1) * self.per_page + 1

    @property
    def end_id(self):
        """Return upper id boundary"""
        return (self.page - 1) * self.per_page + self.per_page

    def paginate(self, model):
        """Build DB query with regards to requested pagination"""
        return (model
                .query
                .filter(and_(model.id >= self.start_id,
                             model.id <= self.end_id)))
